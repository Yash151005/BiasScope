// MongoDB initialization script for BiasScope
// Run with: mongo biasscope init_indexes.js

db = db.getSiblingDB('biasscope');

// Create indexes for analyses collection
db.analyses.createIndex({ "analysis_id": 1 }, { unique: true });
db.analyses.createIndex({ "status": 1 });
db.analyses.createIndex({ "created_at": -1 });
db.analyses.createIndex({ "model_url": 1 });

print("Indexes created successfully for BiasScope database");
