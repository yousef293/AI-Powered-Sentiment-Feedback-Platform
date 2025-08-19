const express=require('express')
const controller=require('./Controllers/controllers')
const mongoose=require('mongoose')
const app=express()
const { body, validationResult } = require('express-validator');
app.use(express.json())
const Url='mongodb+srv://admin:nHLfecsVHTG3Hkgu@cluster0.4pvvsk6.mongodb.net/Sentiment?retryWrites=true&w=majority'
mongoose.connect(Url).then(()=>console.log("the server is connected to db successfully"))



app.use((req,res,next)=>{req.requestTime=new Date().toISOString();
    console.log(`success${req.requestTime}`);next()})

app.get('/test', (req, res) => {
        console.log("everything is good");
        res.send("Test route working!");
    }); 

app.post('/auth/signup',controller.create_user)

app.post('/auth/login',controller.logger)

app.post('/feedback',[
    body("text").notEmpty().escape(),    (req, res, next) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
      next();
    }
],controller.verifyToken,controller.create_feedback)

app.get('/feedback',controller.verifyToken,controller.get_feedbacks)

app.use((req,res)=>{
    res.status(404).json({
        status:"failed",
        message:`The Url: ${req.originalUrl} is not found on server`
    })
})
app.use((err,req,res,next)=>{
    res.status(500).json({
        status:"failed",
        message:`internal server error: ${err}`
    })
})
app.listen(8080)

module.exports=app