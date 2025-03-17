const express = require('express');
const bodyParser = require('body-parser');
const candidateRoutes = require('./routes/candidates');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());

// Routes
app.use('/api', candidateRoutes);

// Test MongoDB connection on startup
async function testConnection() {
  const uri = "mongodb+srv://admin:C5PYrlSjwDCiNVVr@cluster0.wbjpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
  const client = new MongoClient(uri);
  
  try {
    await client.connect();
    console.log("Connected successfully to MongoDB");
    
    // Create the database and collection if they don't exist
    const database = client.db("candidates_db");
    const collection = database.collection("candidates");
    
    console.log("Database and collection initialized");
  } catch (error) {
    console.error("MongoDB connection error:", error);
  } finally {
    await client.close();
  }
}

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  testConnection();
}); 