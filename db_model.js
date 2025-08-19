const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const axios = require('axios');

// Feedback Schema
const feedback_schema = new mongoose.Schema({
    text: {
        type: String,
        required: true,
        maxlength: 200
    },
    createdAt: {
        type: Date,
        default: Date.now
    },
    sentiment: String,
    confidence: Number
});

// Pre-save hook for sentiment analysis
feedback_schema.pre('save', async function (next) {
    try {
        const text = this.text;
        const url = `http://127.0.0.1:8000/predict/${encodeURIComponent(text)}`;
        const response = await axios.get(url);

        // Assuming Python API returns { sentiment: "...", confidence: ... }
        this.sentiment = response.data.sentiment;
        this.confidence = response.data.confidence;

        next();
    } catch (err) {
        next(err); // Pass error to Mongoose
    }
});

// Client Data Schema
const clientdata_schema = new mongoose.Schema({
    user_name: {
        type: String,
        required: true,
        minlength: 3,
        maxlength: 15
    },
    password: {
        type: String,
        required: true,
        minlength: 8,
        maxlength: 20,
        select:false
    }
});

// Pre-save hook to hash password
clientdata_schema.pre('save', async function (next) {
    if (!this.isModified('password')) return next();
    try {
        const salt = await bcrypt.genSalt(12);
        this.password = await bcrypt.hash(this.password, salt);
        next();
    } catch (err) {
        next(err);
    }
});

// Models
const u_database = mongoose.model('Clients_data', clientdata_schema);
const f_database = mongoose.model('Feedback', feedback_schema);

module.exports = { f_database, u_database };
 