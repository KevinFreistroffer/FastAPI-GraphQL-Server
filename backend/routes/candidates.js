const express = require('express');
const router = express.Router();
const { MongoClient, ServerApiVersion } = require('mongodb');

// MongoDB connection URI
const uri = "mongodb+srv://admin:C5PYrlSjwDCiNVVr@cluster0.wbjpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

// POST endpoint to insert candidate
router.post('/candidates', async (req, res) => {
  try {
    // Connect to the MongoDB server
    await client.connect();
    
    // Access the database and collection
    const database = client.db("candidates_db");
    const collection = database.collection("candidates");
    
    // Add timestamp to the data
    const candidateData = {
      ...req.body,
      createdAt: new Date()
    };
    
    // Insert the document
    const result = await collection.insertOne(candidateData);
    
    console.log(`Inserted document with _id: ${result.insertedId}`);
    
    res.status(201).json({ 
      message: 'Candidate inserted successfully', 
      candidateId: result.insertedId 
    });
  } catch (error) {
    console.error('Error inserting candidate:', error);
    res.status(500).json({ error: 'Failed to insert candidate' });
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
});

module.exports = router; 