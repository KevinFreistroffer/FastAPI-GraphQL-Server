import logo from './logo.svg';
import './App.css';
import React, { useState, useRef } from 'react';

function App() {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  const handleAutofill = () => {
    console.log('From state:', text);
    console.log('From ref:', textareaRef.current.value);
    
    // Parse the textarea content
    const textContent = textareaRef.current.value;
    const candidateData = parseTextareaContent(textContent);
    
    // Insert into database
    insertCandidateToMongoDB(candidateData);
  }
  
  // Function to parse the textarea content
  const parseTextareaContent = (content) => {
    // Create an object to store the parsed data
    const data = {};
    
    // Define the fields to extract
    const fields = [
      { key: 'fullName', label: 'Candidate Full Name' },
      { key: 'contactNumber', label: 'Contact Number' },
      { key: 'email', label: 'E-mail ID' },
      { key: 'linkedin', label: 'LinkedIn ID' },
      { key: 'location', label: 'Present location' },
      { key: 'education', label: 'Education Details' },
      { key: 'ssnLast4', label: 'Last 4 digit SSN number' },
      { key: 'dob', label: 'DOB' }
    ];
    
    // Extract each field
    fields.forEach(field => {
      const regex = new RegExp(`${field.label}[^:]*:(.+?)(?=\\n\\s*\\n|$)`, 's');
      const match = content.match(regex);
      data[field.key] = match ? match[1].trim() : '';
    });
    
    return data;
  };
  
  // Function to insert data into MongoDB
  const insertCandidateToMongoDB = async (candidateData) => {
    try {
      // Make API call to your backend service
      const response = await fetch('/api/candidates', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(candidateData),
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Candidate inserted successfully:', result);
        alert('Candidate data saved successfully!');
      } else {
        console.error('Failed to insert candidate data');
        alert('Failed to save candidate data. Please try again.');
      }
    } catch (error) {
      console.error('Error inserting candidate data:', error);
      alert('An error occurred while saving the data.');
    }
  };

  return (
    <div className="App">
      <textarea 
        id="textarea" 
        name="textarea" 
        placeholder="Matrix details ..." 
        onChange={(e) => setText(e.target.value)}
        ref={textareaRef}
      />
      <button type="button" onClick={handleAutofill}>Autofill</button>  
    </div>
  );
}

export default App;
