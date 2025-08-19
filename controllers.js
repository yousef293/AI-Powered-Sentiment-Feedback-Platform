const { f_database, u_database } = require('../Model/db_model');
const jwt=require('jsonwebtoken')
const Secret_key="nduo83hruwi7tibe57tbygbw8h3$E%R^VHBBKBJBKBKJBKB"
const bcrypt=require('bcryptjs');
const { json } = require('express');

exports.create_user = async (req, res) => {
   
    try {
        // const{user_name,password} = req.body;
        const user = new u_database(req.body);
        
        // Check if user_id already exists
        const in_db = await u_database.findOne({ user_name: req.body.user_name});
        if (in_db) {
            return res.json("The user is already in the database");
        }

        // Save new user
        
        const saved_user = await user.save();
        token=jwt.sign({"_id": saved_user._id ,"user_name":saved_user.user_name},Secret_key,{expiresIn:'1h'})
        res.json({saved_user,
            "jwt":token
        });
        
    } catch (err) {
        res.status(500).json({
            status: "failed",
            message: err.message
        });
    }
};

  exports.logger=(async (req,res,next)=>{
    const user = new u_database(req.body);
    const in_db = await u_database.findOne({ user_name: user.user_name }).select('+password');
    if (!in_db) {
        return res.status(404).json("invalid User name");
    }
    const check=await bcrypt.compare(user.password,in_db.password)
    if (!check){
        return res.status(401).json("invalid password")
    }
    token=jwt.sign({"id":in_db._id,"user_name":in_db.user_name},Secret_key,{expiresIn:'1h'})
    res.json({message:"Logged in succefully",
        token,
    })

})


exports.verifyToken=((req, res, next)=> {
    const auth_header = req.headers['authorization'];

    if (!auth_header || !auth_header.toLowerCase().startsWith('bearer ')) {
        return res.status(401).json({
            message: 'Authorization token missing or invalid'
        });
    }

    const token = auth_header.split(' ')[1];

    try {
        const decoded = jwt.verify(token, Secret_key);
        req.user = decoded; // attach user info to request
        next(); // continue to route
    } catch (err) {
        return res.status(403).json({
            status: "failed",
            message: "Invalid or expired token"
        });
    }
})

exports.create_feedback =(async (req, res,next) => {


    try {
        const feedback = new f_database({ text: req.body.text,user_id:req.user._id });
        const saved_feedback = await feedback.save();
        res.json(saved_feedback);
    } catch (err) {
        res.status(500).json({
            status: "failed",
            message: err.message
        });
    }
});
 exports.get_feedbacks=(async (req,res)=>{
    try{
        const data=await f_database.find({user_id:req.user._id})
        res.status(200).json({
            "data":data
        })
    }catch(err){
        res.status(400).json(
            {
                status:"failed",
                message:err.message
            }
        )
    }
 })