from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import string
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Mock database
events_db = [
    {
        "id": 1,
        "title": "Inception",
        "category": "movies",
        "image": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80",
        "rating": 4.8,
        "genre": "Sci-Fi, Thriller",
        "duration": "2h 28m",
        "language": "English",
        "venues": [
            {"id": 1, "name": "PVR Cinemas", "location": "Downtown", "times": ["10:00 AM", "1:30 PM", "5:00 PM", "8:30 PM"]},
            {"id": 2, "name": "INOX Theatre", "location": "Suburb Mall", "times": ["11:00 AM", "2:30 PM", "6:00 PM", "9:30 PM"]}
        ],
        "price": 250
    },
    {
        "id": 2,
        "title": "Coldplay World Tour",
        "category": "concerts",
        "image": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&q=80",
        "rating": 4.9,
        "genre": "Rock, Pop",
        "duration": "3h",
        "language": "English",
        "venues": [
            {"id": 3, "name": "Stadium Arena", "location": "City Center", "times": ["7:00 PM"]}
        ],
        "price": 2500
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "category": "movies",
        "image": "https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=800&q=80",
        "rating": 4.9,
        "genre": "Action, Drama",
        "duration": "2h 32m",
        "language": "English",
        "venues": [
            {"id": 1, "name": "PVR Cinemas", "location": "Downtown", "times": ["12:00 PM", "3:30 PM", "7:00 PM", "10:30 PM"]}
        ],
        "price": 300
    },
    {
        "id": 4,
        "title": "Stand-Up Comedy Night",
        "category": "events",
        "image": "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800&q=80",
        "rating": 4.6,
        "genre": "Comedy",
        "duration": "2h",
        "language": "English, Hindi",
        "venues": [
            {"id": 4, "name": "Comedy Club", "location": "Entertainment District", "times": ["8:00 PM", "10:00 PM"]}
        ],
        "price": 500
    },
    {
        "id": 5,
        "title": "FIFA Championship",
        "category": "sports",
        "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80",
        "rating": 4.7,
        "genre": "Football",
        "duration": "2h",
        "language": "Live",
        "venues": [
            {"id": 5, "name": "Sports Complex", "location": "North End", "times": ["4:00 PM"]}
        ],
        "price": 1500
    },
    {
        "id": 6,
        "title": "Interstellar",
        "category": "movies",
        "image": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800&q=80",
        "rating": 4.9,
        "genre": "Sci-Fi, Adventure",
        "duration": "2h 49m",
        "language": "English",
        "venues": [
            {"id": 2, "name": "INOX Theatre", "location": "Suburb Mall", "times": ["1:00 PM", "4:30 PM", "8:00 PM"]}
        ],
        "price": 280
    }
]

bookings_db = []

def generate_booking_id():
    """Generate a unique booking ID"""
    return 'BK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

# Routes
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events or filter by category"""
    category = request.args.get('category')
    
    if category and category != 'all':
        filtered_events = [e for e in events_db if e['category'] == category]
        return jsonify(filtered_events)
    
    return jsonify(events_db)

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event by ID"""
    event = next((e for e in events_db if e['id'] == event_id), None)
    
    if event:
        return jsonify(event)
    
    return jsonify({"error": "Event not found"}), 404

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    """Create a new booking"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['event_id', 'venue_id', 'time', 'seats']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Find the event
    event = next((e for e in events_db if e['id'] == data['event_id']), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Find the venue
    venue = next((v for v in event['venues'] if v['id'] == data['venue_id']), None)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404
    
    # Validate time
    if data['time'] not in venue['times']:
        return jsonify({"error": "Invalid time slot"}), 400
    
    # Calculate total
    total = event['price'] * data['seats']
    
    # Create booking
    booking = {
        "booking_id": generate_booking_id(),
        "event_id": data['event_id'],
        "event": event['title'],
        "venue_id": data['venue_id'],
        "venue": venue['name'],
        "location": venue['location'],
        "time": data['time'],
        "seats": data['seats'],
        "price": event['price'],
        "total": total,
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    
    bookings_db.append(booking)
    
    return jsonify(booking), 201

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Get all bookings"""
    return jsonify(bookings_db)

@app.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get a specific booking by ID"""
    booking = next((b for b in bookings_db if b['booking_id'] == booking_id), None)
    
    if booking:
        return jsonify(booking)
    
    return jsonify({"error": "Booking not found"}), 404

@app.route('/api/bookings/<booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    global bookings_db
    
    booking = next((b for b in bookings_db if b['booking_id'] == booking_id), None)
    
    if booking:
        bookings_db = [b for b in bookings_db if b['booking_id'] != booking_id]
        return jsonify({"message": "Booking cancelled successfully"}), 200
    
    return jsonify({"error": "Booking not found"}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_events": len(events_db),
        "total_bookings": len(bookings_db)
    })

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "message": "TicketHub API",
        "version": "1.0.0",
        "endpoints": {
            "events": "/api/events",
            "bookings": "/api/bookings",
            "health": "/api/health"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)