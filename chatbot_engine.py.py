"""
Enhanced Chatbot Engine with Advanced NLU and Context Understanding
"""

import re
import random
from datetime import datetime
from typing import Dict, List, Optional
import json

class ChatbotEngine:
    """
    Highly intelligent chatbot engine with:
    - Advanced intent detection
    - Context awareness
    - Conversational memory
    - Multi-turn dialogue handling
    - Semantic understanding
    """
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_contexts = {}
        
    def _load_knowledge_base(self) -> Dict:
        """Load comprehensive knowledge base"""
        return {
            # APPLICATION FORM
            "applicationFormDetails": {
                "keywords": ["application form", "fill application", "student details", "personal details", 
                           "apply", "start application", "how to apply", "application process"],
                "responses": [
                    """In the Application Form page, you need to fill complete student details including:

• Name (First, Middle, Surname)
• Date of Birth
• Class applying for and Academic Year
• Place of Birth, Religion, Caste
• Gender and Blood Group
• Mobile number, Aadhaar number, Email
• Nationality and Mother Tongue
• Residential and Permanent Address
• Parent/Guardian details

You also need to upload the student photo. After filling all mandatory fields, click Submit."""
                ]
            },
            
            # HEALTH FORM
            "healthForm": {
                "keywords": ["health form", "health details", "medical", "chronic disease", 
                           "emergency contact", "hospital", "clinic", "health declaration"],
                "responses": [
                    """After submitting the Application Form, you must fill the Health Form on the right side. This is MANDATORY.

In the Health Form, you need to provide:
• Any chronic diseases or health conditions
• Preferred hospital or clinic
• Emergency contact number
• Health declaration (must be accepted)

Click Submit after completing all health details."""
                ]
            },
            
            # REGISTRATION
            "registration": {
                "keywords": ["registration", "register", "verify details", "check details", 
                           "review application", "registration page"],
                "responses": [
                    """The Registration page is found under the Application Form section. Here you can view and verify all the details you entered in the Application Form including student information, parent details, and uploaded documents. Review everything carefully before proceeding."""
                ]
            },
            
            # DOCUMENT VIEW
            "documentView": {
                "keywords": ["document view", "view documents", "check documents", 
                           "see application", "view form", "application summary"],
                "responses": [
                    """In Document View, you can select the Academic Year and Class to display the submitted application form. This allows you to view your completed application with all details and uploaded documents in one place."""
                ]
            },
            
            # INTERVIEW SCHEDULE
            "interviewSchedule": {
                "keywords": ["interview", "interview schedule", "oral test", "written test", 
                           "test schedule", "exam schedule", "interview date", "test date"],
                "responses": [
                    """Interview Schedule has two sections:

1. **Oral Test Schedule** - Check your oral interview date, time, and venue
2. **Written Test Schedule** - Check your written exam date, time, and venue

Both schedules will be assigned after your application is reviewed. Check regularly for updates."""
                ]
            },
            
            # MARKS ENTRY
            "marksEntry": {
                "keywords": ["marks entry", "enter marks", "scores", "test results", 
                           "oral marks", "written marks", "exam results"],
                "responses": [
                    """Marks Entry has two sections:

1. **Oral Test Entry** - View oral interview scores
2. **Written Test Entry** - View written examination marks

This section is typically filled by the school after you complete both tests. You can check your test scores here."""
                ]
            },
            
            # PREADMISSION STATUS
            "preadmissionStatus": {
                "keywords": ["status", "application status", "admission status", 
                           "check status", "track application", "where to check"],
                "responses": [
                    """Preadmission Status has TWO important sections:

1. **APPLICATION STATUS** with 3 stages:
   • Application Waiting - Under review
   • Application Rejected - Not accepted
   • Application Accepted - Approved for next stage

2. **ADMISSION STATUS** (appears after application is accepted):
   • In Progress - Processing admission
   • Selected - You're selected
   • Rejected - Not selected
   • Confirmed - Admission confirmed

Check this regularly for updates!"""
                ]
            },
            
            # TRANSFER STUDENT
            "transferStudent": {
                "keywords": ["transfer student", "transfer pre admission", "confirmed students", 
                           "final stage", "pre adm to adm"],
                "responses": [
                    """The Transfer Student section has the "Transfer Pre Admission to Admission" page. This shows students whose Admission Status is "Confirmed". 

Select the Academic Year and Class to see the list of confirmed students who are being transferred from pre-admission to final admission. This is the final stage!"""
                ]
            },
            
            # REPORTS
            "reportsModule": {
                "keywords": ["reports", "reports section", "all reports", "download reports"],
                "responses": [
                    """The Reports section contains 5 important reports:

1. **Enquiry Report** - View all student enquiries
2. **Prospectus Report** - School prospectus
3. **Registration Report** - List of registered students
4. **Schedule Report** - Interview and test schedules
5. **Student Count Report** - Statistics by class/year

Select the report type, choose filters, and click Generate/Download."""
                ]
            },
            
            # COMPLETE PROCESS
            "completeProcess": {
                "keywords": ["complete process", "full process", "step by step", 
                           "how to proceed", "process flow", "admission procedure"],
                "responses": [
                    """Complete Pre-Admission Process:

1. Fill Application Form (student + parent details)
2. Fill Health Form (MANDATORY)
3. Verify in Registration page
4. Check Interview Schedule (oral + written)
5. Attend both tests
6. Check Marks Entry for results
7. Monitor Application Status (Waiting → Accepted)
8. Monitor Admission Status (In Progress → Selected → Confirmed)
9. Once Confirmed, you appear in Transfer Student page
10. Download reports from Reports section

Check Preadmission Status regularly for updates!"""
                ]
            }
        }
    
    def _detect_intent(self, user_input: str, conversation_history: List = None) -> Dict:
        """
        Advanced intent detection with context awareness
        Returns: {intent, confidence, entities, context}
        """
        input_lower = user_input.lower().strip()
        
        # Priority 1: COMPLETION + NEXT STEP patterns
        completion_patterns = [
            (r'\b(filled|completed|done|finished|submitted)\b.*\b(application|form|health)\b', 'completion_application'),
            (r'\b(filled|completed|done|finished|submitted)\b.*\b(health|medical)\b', 'completion_health'),
            (r'\b(attended|gave|took|completed|done|finished)\b.*\b(interview|test|exam|oral|written)\b', 'completion_interview'),
            (r'\b(got|received|have|seen)\b.*\b(marks|score|result)\b', 'completion_marks'),
        ]
        
        for pattern, intent in completion_patterns:
            if re.search(pattern, input_lower):
                return {
                    'intent': intent,
                    'confidence': 0.95,
                    'type': 'completion',
                    'entities': self._extract_entities(input_lower)
                }
        
        # Priority 2: SELECTION/RESULT queries
        selection_patterns = [
            r'(how|when|where).*(know|check|see|find).*(selected|got selected|passed|cleared)',
            r'(selected|got selected|passed).*(interview|test|exam)',
            r'(interview|test).*(result|selected|passed|outcome)',
            r'(ward|child|son|daughter).*(selected|got|passed)',
        ]
        
        for pattern in selection_patterns:
            if re.search(pattern, input_lower):
                return {
                    'intent': 'check_selection_result',
                    'confidence': 0.95,
                    'type': 'question',
                    'entities': {'topic': 'selection_result'}
                }
        
        # Priority 3: NEXT STEP queries
        next_step_patterns = [
            r'\b(what|what\'s)\b.*(next|after|then|following)',
            r'\b(after|completed|finished|done)\b.*\b(what|now)',
            r'(next step|what should|what to do)',
            r'(proceed|continue|move forward)',
        ]
        
        for pattern in next_step_patterns:
            if re.search(pattern, input_lower):
                # Check conversation history for context
                if conversation_history:
                    recent_topics = self._analyze_conversation_context(conversation_history)
                    return {
                        'intent': 'next_step_query',
                        'confidence': 0.9,
                        'type': 'next_step',
                        'entities': {'recent_context': recent_topics}
                    }
                
                return {
                    'intent': 'next_step_query',
                    'confidence': 0.8,
                    'type': 'next_step',
                    'entities': {}
                }
        
        # Priority 4: HOW-TO questions
        howto_patterns = [
            (r'how.*(fill|complete|submit)', 'howto_fill'),
            (r'how.*(check|see|view|track|monitor)', 'howto_check'),
            (r'how.*(upload|attach)', 'howto_upload'),
            (r'what.*(health form|application form|registration)', 'what_is'),
        ]
        
        for pattern, intent in howto_patterns:
            if re.search(pattern, input_lower):
                return {
                    'intent': intent,
                    'confidence': 0.85,
                    'type': 'question',
                    'entities': self._extract_entities(input_lower)
                }
        
        # Priority 5: STATUS checking
        if re.search(r'\b(status|track|check|where|see)\b', input_lower):
            return {
                'intent': 'check_status',
                'confidence': 0.8,
                'type': 'question',
                'entities': {'topic': 'status'}
            }
        
        # Priority 6: General information request
        if re.search(r'\b(what|tell|explain|describe|information|details|about)\b', input_lower):
            return {
                'intent': 'information_request',
                'confidence': 0.7,
                'type': 'question',
                'entities': self._extract_entities(input_lower)
            }
        
        return {
            'intent': 'unknown',
            'confidence': 0.3,
            'type': 'unclear',
            'entities': {}
        }
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract important entities from text"""
        entities = {}
        
        # Topic entities
        topics = {
            'application': ['application', 'form', 'apply'],
            'health': ['health', 'medical', 'chronic'],
            'registration': ['registration', 'register', 'verify'],
            'interview': ['interview', 'oral', 'written', 'test', 'exam'],
            'marks': ['marks', 'score', 'result'],
            'status': ['status', 'track', 'progress'],
            'documents': ['document', 'upload', 'photo', 'file'],
            'reports': ['report', 'enquiry', 'prospectus', 'schedule', 'count']
        }
        
        for topic, keywords in topics.items():
            if any(kw in text for kw in keywords):
                entities['topic'] = topic
                break
        
        # Time-related entities
        if re.search(r'\b(next|after|before|then)\b', text):
            entities['temporal'] = 'next_step'
        
        # Family entities
        if re.search(r'\b(ward|child|son|daughter|kid)\b', text):
            entities['subject'] = 'ward'
        
        return entities
    
    def _analyze_conversation_context(self, conversation_history: List) -> List:
        """Analyze recent conversation to understand context"""
        recent_topics = []
        
        # Look at last 3-5 messages
        for msg in conversation_history[-5:]:
            if msg.get('role') == 'user':
                user_text = msg.get('message', '').lower()
                
                # Detect what was mentioned
                if 'application' in user_text or 'form' in user_text:
                    recent_topics.append('application')
                if 'health' in user_text:
                    recent_topics.append('health')
                if 'interview' in user_text or 'test' in user_text:
                    recent_topics.append('interview')
                if 'completed' in user_text or 'finished' in user_text:
                    recent_topics.append('completion')
        
        return list(set(recent_topics))  # Remove duplicates
    
    def _is_off_topic(self, user_input: str) -> bool:
        """Detect if query is off-topic"""
        input_lower = user_input.lower().strip()
        
        # Obviously off-topic keywords
        off_topic_keywords = [
            'weather', 'temperature', 'rain', 'sunny',
            'movie', 'film', 'song', 'music', 'game',
            'food', 'recipe', 'cook', 'restaurant',
            'cricket', 'football', 'sports', 'match',
            'news', 'politics', 'election',
            'shopping', 'buy', 'amazon', 'flipkart',
            'joke', 'story', 'fun',
        ]
        
        # Check for math expressions
        if re.match(r'^\d+\s*[\+\-\*\/]\s*\d+', input_lower):
            return True
        
        # Count off-topic words
        off_topic_count = sum(1 for kw in off_topic_keywords if kw in input_lower)
        
        # Check for admission-related words
        admission_keywords = [
            'application', 'form', 'admission', 'student', 'school',
            'interview', 'test', 'exam', 'marks', 'status',
            'registration', 'health', 'document', 'report'
        ]
        
        admission_count = sum(1 for kw in admission_keywords if kw in input_lower)
        
        # If more off-topic words than admission words, it's off-topic
        if off_topic_count > admission_count and off_topic_count >= 2:
            return True
        
        # If only off-topic words and no admission words
        if off_topic_count > 0 and admission_count == 0 and len(input_lower.split()) <= 5:
            return True
        
        return False
    
    def find_best_response(self, user_input: str, conversation_history: List = None) -> Dict:
        """
        Main method to find best response with full context awareness
        """
        input_lower = user_input.lower().strip()
        
        # Check off-topic FIRST
        if self._is_off_topic(user_input):
            return {
                "response": "I'm sorry, I can only assist with pre-admission related queries. Please ask me about the application process, health form, interview schedules, status checking, reports, or any other pre-admission procedures.",
                "category": "off-topic",
                "confidence": 1.0,
                "intent": "off_topic"
            }
        
        # Greetings
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'namaste']
        if any(input_lower == g or input_lower.startswith(g + ' ') or input_lower.startswith(g + ',') for g in greetings):
            return {
                "response": "Hello! How can I help you with the pre-admission process today? You can ask me about application forms, health forms, interview schedules, status checking, or any step in the admission process.",
                "category": "greeting",
                "confidence": 1.0,
                "intent": "greeting"
            }
        
        # Thank you
        if re.search(r'\b(thank|thanks|appreciate)\b', input_lower):
            return {
                "response": "You're welcome! Feel free to ask if you have any other questions about pre-admission. I'm here to help guide you through the entire process.",
                "category": "gratitude",
                "confidence": 1.0,
                "intent": "gratitude"
            }
        
        # Goodbye
        if re.search(r'\b(bye|goodbye|see you|good night)\b', input_lower):
            return {
                "response": "Goodbye! Best of luck with your admission process. Feel free to return if you have more questions!",
                "category": "farewell",
                "confidence": 1.0,
                "intent": "farewell"
            }
        
        # Detect intent with context
        intent_result = self._detect_intent(user_input, conversation_history)
        
        # Handle based on intent
        if intent_result['intent'] == 'check_selection_result':
            return {
                "response": """After completing your Oral and Written Tests, check the following to see if your ward got selected:

**1. Marks Entry Section**
   • Go to "Marks Entry" page
   • View Oral Test Entry - Your interview scores
   • View Written Test Entry - Your exam marks

**2. Preadmission Status → Admission Status**
   This is where you'll see the SELECTION RESULT:
   • **In Progress** - Tests are being evaluated
   • **Selected** - Congratulations! Your ward is SELECTED! 🎉
   • **Rejected** - Not selected this time
   • **Confirmed** - Final admission confirmed

The **Admission Status** clearly shows if your ward got selected. Keep checking it after completing the interviews!

Would you like to know what happens after getting selected?""",
                "category": "interview-results",
                "confidence": 0.95,
                "intent": "check_selection_result"
            }
        
        elif intent_result['intent'].startswith('completion_'):
            # User completed something, provide next steps
            stage = intent_result['intent'].replace('completion_', '')
            
            next_step_responses = {
                'application': """Perfect! Since you've filled the Application Form, the **next mandatory step** is:

**📋 Fill the Health Form**

The Health Form appears on the right side of the same page. You MUST complete it. It requires:
• Any chronic diseases or health conditions
• Preferred hospital or clinic for emergencies
• Emergency contact number
• Health declaration (mandatory checkbox)

After submitting the Health Form, go to the **Registration Page** to verify all your details.

Need help with the Health Form?""",
                
                'health': """Great! After completing both Application and Health Forms, here's what's next:

**Step 1: Verify Your Details**
Go to the **Registration Page** (under Application Form section) to review all information you've entered.

**Step 2: Wait for Interview Schedule**
The school will review your application (typically 3-5 working days) and assign:
- Oral Test (Interview) - date, time, venue
- Written Test - date, time, venue

**Step 3: Check Interview Schedule Section**
Check the "Interview Schedule" section regularly for your test dates.

**Step 4: Prepare Documents**
Keep all original documents ready for verification during the interview.

Would you like tips on preparing for the interview?""",
                
                'interview': """Excellent! You've completed the tests. Here's what happens next:

**Immediate Next Steps:**

1. **Check Marks Entry (2-3 days)**
   • Go to "Marks Entry" section
   • View Oral Test Entry - Your interview scores
   • View Written Test Entry - Your exam marks

2. **Monitor Preadmission Status (5-7 days)**
   Go to **Preadmission Status** → Check these sections:
   
   **Application Status:**
   • Waiting → Under review
   • **Accepted** → Moves to admission stage ✓
   • Rejected → Not accepted
   
   **Admission Status** (after acceptance):
   • In Progress → Being evaluated
   • **Selected** → You're IN! 🎉
   • **Confirmed** → Final admission confirmed
   • Rejected → Not selected

3. **Keep Checking Daily** for status updates

Need help understanding the status stages?""",
                
                'marks': """Good! Since you've seen your marks, here's what comes next:

**Monitor Your Admission Status:**

Go to **Preadmission Status** page and check:

1. **Application Status**
   Must show "**Accepted**" (if not yet, wait for review)

2. **Admission Status** (appears after acceptance)
   • **In Progress** - Your application is being evaluated
   • **Selected** - Congratulations! You're selected! 🎉
   • **Confirmed** - Your admission is CONFIRMED (final stage)
   • Rejected - Not selected

Once you reach "**Confirmed**" status, you'll appear in the **Transfer Student** section under "Transfer Pre Admission to Admission".

That's the final step before enrollment!

Check the Preadmission Status page regularly for updates."""
            }
            
            response_text = next_step_responses.get(stage, 
                """Great progress! Here are the general next steps:

1. Fill Application Form → Fill Health Form
2. Verify in Registration page
3. Attend Oral and Written Tests
4. Check Marks Entry for scores
5. Monitor Preadmission Status for selection

Which specific stage would you like to know more about?""")
            
            return {
                "response": response_text,
                "category": f"completed-{stage}",
                "confidence": 0.9,
                "intent": intent_result['intent']
            }
        
        elif intent_result['intent'] == 'next_step_query':
            # User asking "what next?" - use conversation context
            context = intent_result.get('entities', {}).get('recent_context', [])
            
            if 'completion' in context or 'interview' in context:
                return {
                    "response": """To give you the right next steps, please tell me what you completed:

- "I filled the application form"
- "I completed the health form"
- "I registered my details"
- "I attended the interview/test"
- "I got my marks"

Just tell me what you finished, and I'll guide you on what comes next!""",
                    "category": "clarify-next-step",
                    "confidence": 0.8,
                    "intent": "clarify_needed"
                }
            else:
                return {
                    "response": """Here's the complete admission process:

**Current Step → Next Step:**

1. **Start** → Fill Application Form
2. **Filled Application** → Fill Health Form (mandatory!)
3. **Filled Health Form** → Verify in Registration page
4. **Registered** → Wait for Interview Schedule → Attend Tests
5. **Attended Tests** → Check Marks Entry → Monitor Application Status
6. **Application Accepted** → Monitor Admission Status
7. **Status = Selected** → Wait for Confirmation
8. **Status = Confirmed** → Go to Transfer Student section
9. **Final** → Enrollment complete!

Which stage are you currently at? I can give you specific guidance!""",
                    "category": "complete-process",
                    "confidence": 0.75,
                    "intent": "process_overview"
                }
        
        # Keyword matching fallback
        best_match = None
        max_score = 0
        
        for category, data in self.knowledge_base.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword.lower() in input_lower:
                    score += len(keyword.split()) * 2
            
            if score > max_score:
                max_score = score
                best_match = category
        
        if best_match and max_score > 0:
            responses = self.knowledge_base[best_match]["responses"]
            return {
                "response": random.choice(responses),
                "category": best_match,
                "confidence": min(max_score / 10, 1.0),
                "intent": "keyword_match"
            }
        
        # Final fallback
        return {
            "response": """I'm here to help with pre-admission! You can ask me:

**About Forms:**
- "How to fill application form?"
- "What is health form?"

**About Status:**
- "How to check my status?"
- "How will I know if selected?"

**About Process:**
- "I filled the form, what next?"
- "Complete admission process?"

**About Reports:**
- "What reports are available?"

What would you like to know?""",
            "category": "help",
            "confidence": 0.4,
            "intent": "unclear_fallback"
        }
    
    def get_all_topics(self) -> List[Dict]:
        """Get all available topics"""
        topics = []
        for key, data in self.knowledge_base.items():
            topics.append({
                "id": key,
                "name": re.sub(r'([A-Z])', r' \1', key).strip().title(),
                "keywords": data["keywords"],
                "response_count": len(data["responses"])
            })
        return topics