"""
IVRM Pre-Admission Chatbot API - Complete Python Implementation
Academic Management System by VASPS
"""

from flask import Flask, request, jsonify , render_template
from flask_cors import CORS
from datetime import datetime
import re
import random
import os
import logging





app = Flask(__name__)
CORS(app)



#@app.route("/")
#def home():
    #return render_template("index.html")
    
if __name__ == "__main__":

    @app.route("/")
    def home():
        return render_template("index.html")
    CORS(app)
# Comprehensive Knowledge Base for IVRM Pre-Admission Module
KNOWLEDGE_BASE = {
    # APPLICATION FORM PAGE
    "applicationFormDetails": {
        "keywords": [
            "application form", "fill application", "student details", 
            "personal details", "apply", "start application", "how to apply", 
            "application process"
        ],
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

You also need to upload the student photo. After filling all mandatory fields, click Submit.""",
            """The Application Form requires comprehensive student information. Fill in personal details like name, DOB, gender, religion, caste, blood group, contact details (mobile, email), addresses (residential and permanent), and parent/guardian information. Don't forget to upload the student photo before submitting."""
        ]
    },
    
    # HEALTH FORM
    "healthForm": {
        "keywords": [
            "health form", "health details", "medical", "chronic disease", "next application","after submitting application form"
            "emergency contact", "hospital", "clinic", "health declaration","form after application form ", "next step after application form"
        ],
        "responses": [
            """After submitting the Application Form, you must fill the Health Form on the right side. This is MANDATORY. In the Health Form, you need to provide:

• Any chronic diseases or health conditions
• Preferred hospital or clinic
• Emergency contact number
• Health declaration (must be accepted)

Click Submit after completing all health details.""",
            """The Health Form appears on the right side after you submit the Application Form. It's a mandatory step where you provide student health information including chronic diseases, preferred hospital/clinic for emergencies, emergency contact number, and you must accept the health declaration before submitting."""
        ]
    },

    # PARENT DETAILS
    "parentDetails": {
        "keywords": [
            "parent details", "father", "mother", "guardian", 
            "parent information", "family details"
        ],
        "responses": [
            """In the Application Form, you need to provide complete parent/guardian details including their names, occupation, contact numbers, and email addresses. This information is important for communication and emergency purposes.""",
            """Parent and guardian details are collected in the Application Form. Fill in father's name, mother's name, their occupations, contact numbers, and email IDs. This helps the school maintain proper communication channels."""
        ]
    },

    # DOCUMENT UPLOAD
    "documentUpload": {
        "keywords": [
            "upload", "document upload", "photo upload", "student photo", 
            "upload picture", "how to upload","where to upload"
        ],
        "responses": [
            """To upload the relevnt documents, click on "Upload Document" button on the bottom side of the Document upload details section in the Application Form. Supported formats are JPG, PNG with maximum size of 2MB. Make sure the photo and other documents are clear""",
            
        ]
    },

    # REGISTRATION PAGE
    "registration": {
        "keywords": [
            "registration", "register", "verify details", "check details", 
            "review application", "registration page", "registration", "register", "verify details", "check details", 
        "review application", "registration page", "where to verify","application form submitted","health form submitted",
        "how to verify", "verify application", "verification","confirm registration","after submitting application form and health form","after submittig application form",
        "where can i check", "where do i review", "review my form",
        "see my application", "look at my details", "confirm details"
        ],
        
        "responses": [
            """The Registration page is found under the Application Form section. Here you can view and verify all the details you entered in the Application Form including student information, parent details, and uploaded documents. Review everything carefully before proceeding.""",
            """After completing the Application and Health forms, go to the Registration page to verify all entered details. This page displays your complete application for review including personal details, address, parent information, and documents. Make sure everything is correct."""
        ]
    },

    # DOCUMENT VIEW
    "documentView": {
        "keywords": [
            "document view", "view documents", "check documents", 
            "see application", "view form", "application summary","submitted documents","verify documents","after registration",
        ],
        "responses": [
            """In Document View, you can select the Academic Year and Class to display the submitted application form. This allows you to view your completed application with all details and uploaded documents in one place.""",
            """Document View lets you check your application by selecting year and class. Once selected, your complete application form will be displayed showing all the information you've submitted including documents and photos."""
        ]
    },

    # INTERVIEW SCHEDULE
    "interviewSchedule": {
        "keywords": [
            "interview", "interview schedule", "oral test", "written test", 
            "test schedule", "exam schedule", "interview date", "test date"
        ],
        "responses": [
            """Interview Schedule has two sections:

            1. Oral Test Schedule - Check your oral interview date, time, and venue
            2. Written Test Schedule - Check your written exam date, time, and venue

            Both schedules will be assigned after your application is reviewed. Check regularly for updates.""",
            """The Interview Schedule section contains your Oral Test Schedule and Written Test Schedule. Once your application is processed, you'll see your assigned dates, times, and venues for both tests here. Make sure to arrive 15 minutes early with required documents."""
        ]
    },

    # ORAL TEST
    "oralTest": {
        "keywords": [
            "oral test", "oral interview", "oral exam", 
            "speaking test", "interview test"
        ],
        "responses": [
            """The Oral Test Schedule shows your personal interview details. Check this section for your scheduled date, time, and venue. Arrive 15 minutes early and bring all original documents for verification. Dress formally and be prepared to answer questions about yourself and academics.""",
            """Your Oral Test (interview) schedule will appear in the Interview Schedule section under "Oral Test Schedule". Note down the date, time, and venue carefully. Original documents may be verified during the interview."""
        ]
    },

    # WRITTEN TEST
    "writtenTest": {
        "keywords": [
            "written test", "written exam", "entrance test", 
            "entrance exam", "exam date"
        ],
        "responses": [
            """The Written Test Schedule displays your entrance examination details. Check the date, time, venue, and subjects to be covered. Bring necessary stationery and admit card if provided. Reach the venue at least 30 minutes before the exam starts.""",
            """Your Written Test details are in the Interview Schedule section under "Written Test Schedule". This shows when and where you need to appear for the entrance examination. Prepare according to the class you're applying for."""
        ]
    },

    # MARKS ENTRY
    "marksEntry": {
        "keywords": [
            "marks entry", "enter marks", "scores", "test results", 
            "oral marks", "written marks", "exam results"
        ],
        "responses": [
            """Marks Entry has two sections:

1. Oral Test Entry - Enter or view oral interview scores
2. Written Test Entry - Enter or view written examination marks

This section is typically filled by the school after you complete both tests. You can check your test scores here.""",
            """The Marks Entry section contains both Oral Test Entry and Written Test Entry. After completing your tests, the school will update your scores here. You can check this section to see how you performed in both the oral interview and written examination."""
        ]
    },

    # PREADMISSION STATUS
    "preadmissionStatus": {
        "keywords": [
            "status", "application status", "admission status", 
            "check status", "track application", "where to check", 
            "application progress"
        ],
        "responses": [
            """Preadmission Status has TWO important sections:

1. APPLICATION STATUS with 3 stages:
   • Application Waiting - Under review
   • Application Rejected - Not accepted
   • Application Accepted - Approved for next stage

2. ADMISSION STATUS (appears after application is accepted):
   • In Progress - Processing admission
   • Selected - You're selected
   • Rejected - Not selected
   • Confirmed - Admission confirmed

Check this regularly for updates!""",
            """To track your application, go to Preadmission Status. First check "Application Status" - it will show Waiting, Rejected, or Accepted. Once Accepted, it moves to "Admission Status" showing In Progress, Selected, Rejected, or Confirmed. This tells you exactly where you stand in the admission process."""
        ]
    },

    # APPLICATION STATUS
    "applicationStatus": {
        "keywords": [
            "application waiting", "application rejected", 
            "application accepted", "application pending", "under review"
        ],
        "responses": [
            """Application Status shows three stages:

• Application Waiting - Your application is under review by the admission committee
• Application Rejected - Your application was not accepted (reasons will be provided)
• Application Accepted - Congratulations! Your application is approved and moves to admission stage

Once accepted, check the Admission Status section.""",
            """In the Application Status section, "Waiting" means your application is being reviewed, "Rejected" means it wasn't accepted, and "Accepted" means you've cleared the first stage. After acceptance, your status moves to the Admission Status section."""
        ]
    },

    # ADMISSION STATUS
    "admissionStatus": {
        "keywords": [
            "admission status", "in progress", "selected", "confirmed", 
            "admission confirmed", "final status"
        ],
        "responses": [
            """Admission Status appears AFTER your application is accepted. It has 4 stages:

• In Progress - Admission processing ongoing (tests, verification)
• Selected - You're selected for admission
• Rejected - Not selected for admission
• Confirmed - Your admission is CONFIRMED! Next step: go to Transfer Student page

Once Confirmed, you'll appear in the Transfer Pre Admission to Admission page.""",
            """After your application is accepted, monitor the Admission Status section. "In Progress" means you're being evaluated through tests and verification. "Selected" means you made it! "Confirmed" is the final stage - your seat is secured. Students with Confirmed status will appear in the Transfer Student section."""
        ]
    },

    # TRANSFER STUDENT
    "transferStudent": {
        "keywords": [
            "transfer student", "transfer pre admission", "confirmed students", 
            "final stage", "admission confirmed", "pre adm to adm"
        ],
        "responses": [
            """The Transfer Student section has the "Transfer Pre Admission to Admission" page. This shows students whose Admission Status is "Confirmed". Select the Academic Year and Class to see the list of confirmed students who are being transferred from pre-admission to final admission. This is the final stage!""",
            """After your Admission Status shows "Confirmed" in the Preadmission Status page, you'll appear in the Transfer Student section under "Transfer Pre Admission to Admission". School admin can select the year and class to see all confirmed students. This marks the completion of your pre-admission process!"""
        ]
    },

    # REPORTS MODULE
    "reportsModule": {
        "keywords": [
            "reports", "reports section", "all reports", "download reports", 
            "generate reports", "reports module"
        ],
        "responses": [
            """The Reports section contains 5 important reports:

1. **Enquiry Report** - View all student enquiries and interested applicants
2. **Prospectus Report** - Generate and download school prospectus
3. **Registration Report** - List of all registered students
4. **Schedule Report** - Interview and test schedules
5. **Student Count Report** - Statistics and count of students by class/year

Select the report type you need, choose filters (year/class), and click Generate/Download.""",
            """Access the Reports section to generate various pre-admission reports. Available reports include Enquiry Report, Prospectus Report, Registration Report, Schedule Report, and Student Count Report. You can filter by academic year and class, then download as PDF or Excel."""
        ]
    },

    # ENQUIRY REPORT
    "enquiryReport": {
        "keywords": [
            "enquiry report", "enquiry", "interested students", 
            "enquiries", "prospective students"
        ],
        "responses": [
            """The Enquiry Report shows all student enquiries and expressions of interest. This report includes:

• Student name and contact details
• Enquiry date
• Class of interest
• Follow-up status
• Conversion status (enquiry to application)

Useful for tracking potential admissions and follow-ups.""",
            """Access the Enquiry Report from the Reports section to view all prospective students who have made enquiries. You can filter by date range, class, and status. This helps track which enquiries have converted to applications."""
        ]
    },

    # PROSPECTUS REPORT
    "prospectusReport": {
        "keywords": [
            "prospectus report", "prospectus", "school prospectus", 
            "brochure", "school information"
        ],
        "responses": [
            """The Prospectus Report allows you to generate and download the school prospectus. This comprehensive document includes:

• School information and facilities
• Academic programs
• Fee structure
• Admission criteria
• Important dates
• Contact information

You can download it as PDF to share with prospective parents.""",
            """Generate the school prospectus from the Prospectus Report section. This official document contains complete information about the school, admission process, fee structure, and facilities. Download and print for distribution to interested parents."""
        ]
    },

    # REGISTRATION REPORT
    "registrationReport": {
        "keywords": [
            "registration report", "registered students", 
            "registration list", "enrolled students"
        ],
        "responses": [
            """The Registration Report displays all students who have completed registration. This report shows:

• Student name and registration number
• Class and section
• Registration date
• Application status
• Payment status
• Document submission status

Filter by academic year, class, and date range. Export to Excel or PDF.""",
            """Access the Registration Report to view all registered students. Select academic year and class to filter results. The report includes registration numbers, student details, payment status, and document verification status. Useful for tracking the registration pipeline."""
        ]
    },

    # SCHEDULE REPORT
    "scheduleReport": {
        "keywords": [
            "schedule report", "interview schedule report", 
            "test schedule", "exam schedule report"
        ],
        "responses": [
            """The Schedule Report shows all interview and test schedules. This report includes:

• Oral Test schedules (date, time, venue)
• Written Test schedules
• Student names and application numbers
• Attendance status
• Venue allocation

Filter by date, class, or test type. Download to share with staff and students.""",
            """Generate the Schedule Report to view all oral and written test schedules. Filter by date range and class. The report helps coordinate interview schedules, manage venues, and track attendance. Export as PDF or Excel for easy distribution."""
        ]
    },

    # STUDENT COUNT REPORT
    "studentCountReport": {
        "keywords": [
            "student count report", "count report", "statistics", 
            "student statistics", "admission statistics", "how many students"
        ],
        "responses": [
            """The Student Count Report provides statistics and analytics:

• Total applications received
• Class-wise student count
• Gender distribution
• Application status breakdown (Waiting/Accepted/Rejected)
• Admission status breakdown (In Progress/Selected/Confirmed)
• Monthly admission trends
• Conversion rates (enquiry to admission)

Great for understanding admission patterns and planning.""",
            """Access the Student Count Report for comprehensive admission statistics. View total counts by class, gender, status, and date range. The report includes visual charts and graphs showing admission trends, helping with capacity planning and decision making."""
        ]
    },

    # COMPLETE PROCESS
    "completeProcess": {
        "keywords": [
            "complete process", "full process", "step by step", 
            "how to proceed", "what next", "process flow", 
            "admission procedure","full procedure"
        ],
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
10. Download reports as needed from Reports section

Check Preadmission Status regularly for updates.""",
            """Here's your admission journey:

Start: Application Form → Health Form → Registration (verify)
Then: Attend Oral & Written Tests (check Interview Schedule)
Next: View scores in Marks Entry
Track: Application Status (must be Accepted)
Final: Admission Status (In Progress → Selected → Confirmed)
End: Transfer Pre Admission to Admission
Reports: Access various reports for documentation

Use Document View anytime to see your form. Check Preadmission Status frequently!"""
        ]
    },

    # FEES
    "fees": {
        "keywords": [
            "fee", "fees", "payment", "pay", "cost", 
            "amount", "charges", "how much"
        ],
        "responses": [
            """Fee details will be displayed during the registration process. Payment can be made online through the portal. After payment, download your receipt from the Reports section. Check Preadmission Status for payment confirmation. Different fees may apply at application stage and after confirmation.""",
            """Application and admission fees are shown at respective stages. You can pay online through the portal. Always download the fee receipt from Reports section. Check Preadmission Status to confirm your payment has been recorded."""
        ]
    },

    # MANDATORY FIELDS
    "mandatoryFields": {
        "keywords": [
            "mandatory", "required", "must fill", 
            "compulsory", "necessary fields"
        ],
        "responses": [
            """Mandatory fields are marked with an asterisk (*) in the Application Form. All mandatory fields must be filled before you can submit. This includes student name, DOB, class, gender, addresses, parent details, and student photo. The Health Form is also MANDATORY after the Application Form.""",
            """Fields marked with * are required. You cannot submit the form without completing these. Both Application Form and Health Form must be fully completed as they are mandatory for processing your admission."""
        ]
    }
}

import nltk
nltk.data.path.insert(0, 'P:/nltk_data')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

"""
Enhanced ChatbotEngine with better context understanding
Replace the ChatbotEngine class in your code with this one
"""

class ChatbotEngine:
    """Intelligent chatbot with proper intent understanding and context-aware detection"""
    
    def __init__(self):
        self.knowledge_base = KNOWLEDGE_BASE
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Pre-admission related vocabulary (expanded)
        self.domain_vocabulary = {
            'application', 'form', 'health', 'student', 'admission', 'school',
            'interview', 'test', 'oral', 'written', 'marks', 'score', 'exam',
            'registration', 'register', 'document', 'upload', 'photo', 'parent',
            'guardian', 'status', 'accepted', 'rejected', 'selected', 'confirmed',
            'schedule', 'date', 'time', 'venue', 'report', 'prospectus', 'enquiry',
            'fee', 'payment', 'transfer', 'class', 'year', 'academic', 'fill',
            'submit', 'complete', 'attend', 'check', 'verify', 'monitor','filled'
            'procedure', 'process', 'step', 'next', 'after', 'before', 'help',
            'guide', 'information', 'details', 'required', 'mandatory', 'medical',
            'chronic', 'disease', 'emergency', 'hospital', 'clinic', 'aadhaar',
            'email', 'mobile', 'address', 'birth', 'religion', 'caste', 'blood',
            'nationality', 'language', 'gender', 'age', 'filled', 'completed',
            'done', 'finished', 'submitted', 'what', 'how', 'when', 'where'
        }
        
        # Off-topic categories (only truly irrelevant topics)
        self.off_topic_categories = {
            'math_calculation': [r'\d+\s*[\+\-\*\/]\s*\d+'],  # Only pure math
            'weather': ['weather', 'temperature', 'rain', 'sunny', 'cloudy', 'forecast'],
            'entertainment': ['movie', 'film', 'song', 'music', 'game', 'actor', 'celebrity'],
            'food': ['recipe', 'cook', 'restaurant', 'dish', 'meal'],
            'sports': ['football', 'cricket', 'basketball', 'tennis', 'tournament'],
            'travel': ['vacation', 'hotel', 'flight', 'booking', 'tourist'],
            'shopping': ['amazon', 'flipkart', 'shopping', 'discount', 'sale'],
            'technology': ['phone', 'laptop', 'android', 'ios', 'windows'],
        }
        
        # Completion indicators (expanded)
        self.completion_indicators = {
            'filled', 'completed', 'done', 'finished', 'submitted',
            'attended', 'gave', 'took', 'got', 'received', 'have',
            'did', 'made', 'uploaded', 'registered'
        }
        
        # Next step indicators
        self.next_step_indicators = {
            'next', 'after', 'then', 'now', 'what now', 'proceed', 
            'following', 'afterward', 'subsequently'
        }
        
        # User state detection patterns (more flexible)
        self.state_patterns = {
            'application_form': [
                r'\b(filled|completed|submitted|done|finished).{0,20}(application|form)\b',
                r'\b(application|form).{0,20}(filled|completed|submitted|done|finished)\b',
                r'\bfilled.{0,10}application\b',
                r'\bcompleted.{0,10}form\b'
            ],
            'health_form': [
                r'\b(filled|completed|submitted|done).{0,20}health.{0,10}form\b',
                r'\bhealth.{0,10}form.{0,20}(filled|completed|submitted|done)\b',
                r'\bcompleted.{0,10}health\b'
            ],
            'registration': [
                r'\b(registered|verified|completed|done).{0,20}(registration|details)\b',
                r'\bregistration.{0,20}(completed|done|finished)\b'
            ],
            'interview_completed': [
                r'\b(attended|gave|took|completed|finished|done).{0,20}(interview|test|exam)\b',
                r'\b(interview|test|exam).{0,20}(attended|done|completed|over|finished)\b'
            ],
            'marks_received': [
                r'\b(got|received|have|seen).{0,20}marks\b',
                r'\bmarks.{0,20}(received|got)\b'
            ]
        }
        
        # Next step responses
        self.next_steps = {
            'application_form': """Perfect! Since you've filled the Application Form, the **next mandatory step** is:

**📋 Fill the Health Form**

The Health Form appears on the right side after submitting the Application Form. You need to provide:
• Any chronic diseases or health conditions
• Preferred hospital or clinic for emergencies
• Emergency contact number
• Accept the health declaration (mandatory checkbox)

After completing the Health Form, you can verify all details in the **Registration Page**.

Need help with the Health Form?""",
            
            'health_form': """Great! After completing the Health Form, here's what comes next:

**✅ Step 1: Verify Your Details**
Go to the **Registration Page** to review all information you've entered

**⏳ Step 2: Wait for Interview Schedule**
The school will review your application (typically 3-5 days) and assign:
• Oral Test (Interview) - date, time, venue
• Written Test - date, time, venue

**📅 Step 3: Check Interview Schedule Section**
Regularly monitor this section for your test dates

**📄 Step 4: Prepare Documents**
Keep all original documents ready for verification

Would you like to know what to expect in the interviews?""",
            
            'registration': """Since you've completed registration, your next steps are:

**1. Monitor Interview Schedule**
Check the "Interview Schedule" section regularly for:
• Oral Test Schedule (your interview date/time/venue)
• Written Test Schedule (your exam date/time/venue)

**2. Prepare for Tests**
• Oral Test: Be ready to discuss yourself, academics, interests
• Written Test: Study according to the class you're applying for

**3. Keep Documents Ready**
Original documents may be verified during the oral interview

The school typically assigns interview dates within 5-7 working days.

Need tips for interview preparation?""",
            
            'interview_completed': """Excellent! You've completed the tests. Here's what happens next:

**Immediate Next Steps:**

1. **Check Marks Entry (2-3 days)**
   • Oral Test Entry - Your interview scores
   • Written Test Entry - Your exam marks

2. **Monitor Application Status (5-7 days)**
   Go to **Preadmission Status** → **Application Status**
   • Waiting → Under review
   • Accepted → You move to next stage ✓
   • Rejected → Not accepted (reasons provided)

3. **Once Accepted → Check Admission Status**
   • In Progress → Being evaluated
   • Selected → You're IN! 🎉
   • Confirmed → Final admission confirmed

Keep checking daily for updates!""",
            
            'marks_received': """Good! Now that you have your test marks, here's what to do:

**Monitor Your Application Status:**
Go to **Preadmission Status** page and check:

**1. Application Status Section:**
• Waiting - Under review by admission committee
• Accepted - Move to next stage
• Rejected - Not selected (reasons provided)

**2. Once Accepted → Admission Status Section:**
• In Progress - Being evaluated
• Selected - Congratulations! You're selected
• Confirmed - Final admission confirmed

**3. After Confirmation:**
• You'll appear in Transfer Student section
• Complete any remaining formalities

Check the status daily for updates!"""
        }
    def extract_intent_and_entities(self, user_input):
        """Extract what user wants (intent) and what they're talking about (entities)"""
        input_lower = user_input.lower()
        tokens = word_tokenize(input_lower)
    
    # Intent detection (what does user want to do?)
        intents = {
            'locate': ['where', 'which page', 'which section', 'find', 'locate'],
            'verify': ['verify', 'check', 'review', 'confirm', 'validate'],
            'understand': ['what is', 'what are', 'explain', 'tell me about', 'describe'],
            'process': ['how to', 'how do i', 'how can i', 'steps to', 'way to'],
            'status': ['status', 'progress', 'stage', 'where am i', 'what stage'],
            'next': ['next', 'after this', 'then what', 'what now', 'proceed'],
            'upload': ['upload', 'attach', 'submit document', 'add file'],
            'fill': ['fill', 'complete', 'enter', 'provide'],
            'schedule': ['when', 'date', 'time', 'schedule', 'appointment']
        }
    
        detected_intent = None
        for intent, keywords in intents.items():
            if any(kw in input_lower for kw in keywords):
                detected_intent = intent
                break
    
    # Entity detection (what are they asking about?)
        entities = {
            'application_form': ['application', 'form', 'student details', 'personal info'],
            'health_form': ['health form', 'medical', 'health details', 'chronic disease'],
            'registration': ['registration', 'verify', 'review page'],
            'interview': ['interview', 'oral test', 'written test', 'exam', 'test'],
            'marks': ['marks', 'scores', 'results', 'grades'],
            'status': ['status', 'application status', 'admission status'],
            'documents': ['document', 'photo', 'upload', 'file', 'picture'],
            'parent': ['parent', 'father', 'mother', 'guardian'],
            'fees': ['fee', 'payment', 'cost', 'charges']
        }
    
        detected_entities = []
        for entity, keywords in entities.items():
            if any(kw in input_lower for kw in keywords):
                detected_entities.append(entity)
    
        return detected_intent, detected_entities
    
    def generate_contextual_response(self, intent, entities, user_input):
        """Generate response based on intent and entities"""
    
        # LOCATE intent - user asking "where"
        if intent == 'locate':
            if 'registration' in entities or 'verify' in user_input.lower():
                return self.knowledge_base['registration']['responses'][0]
            elif 'health_form' in entities:
                return "The Health Form appears on the **right side** after you submit the Application Form. It's mandatory!"
            elif 'marks' in entities:
                return "Check your marks in the **Marks Entry** section - it has both Oral Test Entry and Written Test Entry."
            elif 'status' in entities:
                return "Track your progress in **Preadmission Status** page. It shows both Application Status and Admission Status."
            elif 'interview' in entities:
                return "Your interview details are in the **Interview Schedule** section with Oral and Written test schedules."
    
    # VERIFY intent - user wants to check/confirm
        elif intent == 'verify':
            if 'application_form' in entities or 'registration' in entities:
                return self.knowledge_base['registration']['responses'][0]
            elif 'status' in entities:
                return self.knowledge_base['preadmissionStatus']['responses'][0]
            elif 'marks' in entities:
                return self.knowledge_base['marksEntry']['responses'][0]
    
    # UNDERSTAND intent - user asking "what is"
        elif intent == 'understand':
            if 'health_form' in entities:
                return self.knowledge_base['healthForm']['responses'][0]
            elif 'application_form' in entities:
                return self.knowledge_base['applicationFormDetails']['responses'][0]
            elif 'status' in entities:
                return self.knowledge_base['preadmissionStatus']['responses'][0]
            elif 'interview' in entities:
                return self.knowledge_base['interviewSchedule']['responses'][0]
    
    # PROCESS intent - user asking "how to"
        elif intent == 'process':
            if 'application_form' in entities:
                return self.knowledge_base['applicationFormDetails']['responses'][0]
            elif 'health_form' in entities:
                return self.knowledge_base['healthForm']['responses'][0]
            elif 'upload' in entities or 'documents' in entities:
                return self.knowledge_base['documentUpload']['responses'][0]
            elif 'verify' in user_input.lower():
                return self.knowledge_base['registration']['responses'][1]
    
    # SCHEDULE intent - user asking "when"
        elif intent == 'schedule':
            if 'interview' in entities:
                return self.knowledge_base['interviewSchedule']['responses'][0]
    
    # FILL intent - user wants to complete something
        elif intent == 'fill':
            if 'health_form' in entities:
                return self.knowledge_base['healthForm']['responses'][0]
            elif 'application_form' in entities:
                return self.knowledge_base['applicationFormDetails']['responses'][0]
    
        return None
    
    
    def is_off_topic(self, user_input):
        """Detect if query is truly off-topic (very strict now)"""
        input_lower = user_input.lower().strip()
        
        # Check for pure mathematical calculations
        if re.match(r'^\d+\s*[\+\-\*\/]\s*\d+\s*$', input_lower):
            return True
        
        # Check only for clearly off-topic keywords
        off_topic_keywords = [
            'weather', 'movie', 'film', 'song', 'recipe', 'cook',
            'cricket', 'football', 'game', 'vacation', 'hotel',
            'amazon', 'flipkart', 'phone', 'laptop'
        ]
        
        # Count admission-related vs off-topic words
        admission_words = sum(1 for word in self.domain_vocabulary if word in input_lower)
        off_topic_words = sum(1 for word in off_topic_keywords if word in input_lower)
        
        # Only mark as off-topic if no admission words and has off-topic words
        if off_topic_words > 0 and admission_words == 0:
            return True
        
        return False
    
    def detect_user_state(self, user_input):
        """Detect what stage the user completed using regex patterns"""
        input_lower = user_input.lower()
        
        for state, patterns in self.state_patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    return state
        
        return None
    
    def is_asking_next_step(self, user_input):
        """Check if user is asking about next steps"""
        input_lower = user_input.lower()
        
        # Direct next step questions
        next_patterns = [
            r'\bwhat.{0,10}next',
            r'\bnext.{0,10}step',
            r'\bwhat.{0,10}(after|now|then)',
            r'\bafter.{0,10}(this|that)',
            r'\bthen.{0,10}what',
            r'\bwhat.{0,10}should.{0,10}(i|we|do)',
            r'\bwhat.{0,10}to.{0,10}do',
            r'\bhow.{0,10}(to.{0,10})?proceed'
        ]
        
        return any(re.search(pattern, input_lower) for pattern in next_patterns)
    
    def detect_question_topic(self, user_input):
        """Detect what topic the user is asking about"""
        input_lower = user_input.lower()
    
    # Priority-based topic detection
        topic_patterns = {
            'registration': [  # ADD THIS AT THE TOP - HIGHEST PRIORITY
                r'\bwhere.{0,15}(verify|check|review)',
                r'\b(verify|check|review).{0,15}(application|form|details)',
                r'\bhow.{0,10}(to.{0,10})?(verify|check)',
                r'\bverification.{0,10}(page|section)',
                r'\bverify.{0,10}my.{0,10}(details|application)',
            ],
            'healthForm': [
                r'\bhealth\s+form\b',
                r'\bhealth\s+details\b',
                r'\bmedical\s+form\b',
                r'\bchronic\s+disease\b',
                r'\bemergency\s+contact\b'
            ],
            'applicationFormDetails': [
                r'\bapplication\s+form\b',
                r'\bfill\s+application\b',
                r'\bstudent\s+details\b',
                r'\bpersonal\s+details\b'
            ],
            'interviewSchedule': [
                r'\binterview\s+schedule\b',
                r'\btest\s+schedule\b',
                r'\bexam\s+schedule\b'
            ],
            'oralTest': [
                r'\boral\s+test\b',
                r'\boral\s+interview\b',
                r'\boral\s+exam\b'
            ],
            'writtenTest': [
                r'\bwritten\s+test\b',
                r'\bwritten\s+exam\b',
                r'\bentrance\s+test\b'
            ],
            'preadmissionStatus': [
                r'\bstatus\b',
                r'\bapplication\s+status\b',
                r'\badmission\s+status\b',
                r'\btrack\s+application\b'
            ],
            'marksEntry': [
                r'\bmarks\b',
                r'\bscores\b',
                r'\btest\s+results\b'
            ],
            'registration': [
                r'\bregistration\b',
                r'\bregister\b',
                r'\bverify\s+details\b'
            ],
            'documentUpload': [
                r'\bupload\b',
                r'\bphoto\b',
                r'\bdocument\b'
            ],
            'parentDetails': [
                r'\bparent\b',
                r'\bguardian\b',
                r'\bfather\b',
                r'\bmother\b'
            ],
            'transferStudent': [
                r'\btransfer\b',
                r'\bconfirmed\s+students\b'
            ],
            'fees': [
                r'\bfee\b',
                r'\bpayment\b',
                r'\bcost\b',
                r'\bamount\b'
            ],
            'completeProcess': [
                r'\bcomplete\s+process\b',
                r'\bfull\s+process\b',
                r'\bstep\s+by\s+step\b',
                r'\ball\s+steps\b'
            ]
        }
        
        # Check patterns in priority order
        for topic, patterns in topic_patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower):
                    return topic
        
        # Fallback to simple keyword matching
        simple_keywords = {
            'health': 'healthForm',
            'application': 'applicationFormDetails',
            'interview': 'interviewSchedule',
            'oral': 'oralTest',
            'written': 'writtenTest',
            'marks': 'marksEntry',
            'status': 'preadmissionStatus',
            'registration': 'registration',
            'register': 'registration',
            'upload': 'documentUpload',
            'parent': 'parentDetails',
            'transfer': 'transferStudent',
            'fee': 'fees',
            'payment': 'fees',
            'process': 'completeProcess'
        }
        
        for keyword, topic in simple_keywords.items():
            if keyword in input_lower:
                return topic
        
        return None
    
    def find_best_response(self, user_input, conversation_history=None):
        """Main response logic with context awareness"""
        input_lower = user_input.lower().strip()
        
        # Quick exit for empty input
        if not input_lower:
            return {
                "response": "I didn't receive any message. How can I help you with the pre-admission process?",
                "category": "empty",
                "confidence": 1.0
            }
        
        # Check off-topic (very strict now)
        if self.is_off_topic(user_input):
            return {
                "response": "I'm sorry, I can only assist with pre-admission related queries. Please ask me about the application process, health form, interview schedules, status checking, reports, or any other pre-admission procedures.",
                "category": "off-topic",
                "confidence": 1.0
            }
        # Reformulate vague questions using context
        vague_patterns = ['about that', 'about this', 'about it', 'more info', 'details']
        if any(pattern in input_lower for pattern in vague_patterns):
            if conversation_history:
                # Get last bot response to understand context
                for msg in reversed(conversation_history[-3:]):
                    if msg.get('role') == 'assistant':
                        last_category = msg.get('category', '')
                    if last_category in self.knowledge_base:
                        responses = self.knowledge_base[last_category]['responses']
                        return {
                            "response": random.choice(responses),
                            "category": last_category,
                            "confidence": 0.95,
                            "intent": "continuation_from_context"
                        }
        # Greetings
        greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 
                     'good afternoon', 'good evening', 'namaste']
        if any(input_lower == g or input_lower.startswith(g + ' ') for g in greetings):
            return {
                "response": "Hello! How can I help you with the pre-admission process today? You can ask me about application forms, health forms, interview schedules, status checking, or any step in the admission process.",
                "category": "greeting",
                "confidence": 1.0
            }
        
        # Thank you
        if re.search(r'\b(thank|thanks|appreciate)\b', input_lower):
            return {
                "response": "You're welcome! Feel free to ask if you have any other questions about pre-admission. I'm here to help!",
                "category": "gratitude",
                "confidence": 1.0
            }
        
        # Goodbye
        if re.search(r'\b(bye|goodbye|see you|good night)\b', input_lower):
            return {
                "response": "Goodbye! Best of luck with your admission process. Feel free to return if you have more questions!",
                "category": "farewell",
                "confidence": 1.0
            }
        
        # PRIORITY 1: Check if user completed something AND asking next step
        detected_state = self.detect_user_state(user_input)
        is_next_question = self.is_asking_next_step(user_input)
        
        if detected_state and is_next_question:
            # User said "I filled X, what next?"
            if detected_state in self.next_steps:
                return {
                    "response": self.next_steps[detected_state],
                    "category": f"next-after-{detected_state}",
                    "confidence": 1.0,
                    "intent": "completion_with_next_question",
                    "user_state": detected_state
                }
        
        # PRIORITY 2: Check if just stating completion
        if detected_state and not is_next_question:
            # User just said "I filled the application"
            if detected_state in self.next_steps:
                return {
                    "response": self.next_steps[detected_state],
                    "category": f"completed-{detected_state}",
                    "confidence": 1.0,
                    "intent": "completion_stated",
                    "user_state": detected_state
                }
        
        # PRIORITY 3: Asking next step without stating what they completed
# PRIORITY 3: Asking next step without stating what they completed
        if is_next_question and not detected_state:
        # Check conversation history for context
            if conversation_history:
                for msg in reversed(conversation_history[-5:]):
                    if msg.get('role') == 'user':
                        user_msg = msg.get('message', '')
                # Check for state
                        hist_state = self.detect_user_state(msg.get(user_msg))
                        if hist_state and hist_state in self.next_steps:
                            return {
                                "response": self.next_steps[hist_state],
                                "category": f"next-from-history-{hist_state}",
                                "confidence": 0.9,
                                "intent": "next_step_from_context",
                                "detected_state": hist_state
                            }
                        try:
                            hist_intent, hist_entities = self.extract_intent_and_entities(user_msg)
                        except:
                            hist_intent, hist_entities = None, []
               
                        if hist_entities:
                    # Map entity to next step
                            entity_to_state = {
                                'application_form': 'application_form',
                                'health_form': 'health_form',
                                'registration': 'registration',
                                'interview': 'interview_completed',
                                'marks': 'marks_received'
                    }
                            for entity in hist_entities:
                                if entity in entity_to_state:
                                    state = entity_to_state[entity]
                                    if state in self.next_steps:
                                        return {
                                        "response": f"Based on our conversation about {entity.replace('_', ' ')}, here's what's next:\n\n{self.next_steps[state]}",
                                        " category": f"next-from-entity-{entity}",
                                        "confidence": 0.85,
                                        "intent": "next_step_from_entity_context"
                                    }
            
            # No context found, ask for clarification
            return {
            "response": """To guide you on the next steps, could you tell me which stage you're at?

Please say something like:
• "I filled the application form"
• "I completed the health form"
• "I registered my details"
• "I attended the interview"
• "I got my test marks"

What did you last complete?""",
                "category": "clarify-stage",
                "confidence": 1.0,
                "intent": "next_step_needs_context"
            }
        
# PRIORITY 4: Semantic understanding - intent + entities
        intent, entities = self.extract_intent_and_entities(user_input)
        if intent and entities:
            contextual_response = self.generate_contextual_response(intent, entities, user_input)
            if contextual_response:
                entity_str = '-'.join(entities[:2])  # Max 2 entities
                return {
                    "response": contextual_response,
                    "category": f"{intent}-{entity_str}",
                    "confidence": 1.0,
                    "intent": f"semantic_{intent}",
                    "entities": entities
                }

# PRIORITY 5: Check if asking about a specific topic (pattern matching fallback)
        topic = self.detect_question_topic(user_input)
        if topic and topic in self.knowledge_base:
            responses = self.knowledge_base[topic]["responses"]
            return {
                "response": random.choice(responses),
                "category": topic,
                "confidence": 0.9,
                "intent": "topic_question"
            }
        
    #PRIORITY 5: Keyword matching fallback

        best_match = None
        max_score = 0

        for category, data in self.knowledge_base.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword.lower() in input_lower:
                    # More weight for longer, more specific keywords
                    score += len(keyword.split()) * 2

            if score > max_score:
                max_score = score
                best_match = category

        if best_match and max_score > 0:
            responses = self.knowledge_base[best_match]["responses"]
            return {
                "response": random.choice(responses),
                "category": best_match,
                "confidence": max_score / 10,
                "intent": "keyword_match"
            }
        
        # FINAL FALLBACK
        return {
            "response": """I can help you with:

• **Application Form** - How to fill student and parent details
• **Health Form** - What medical information is needed
• **Registration** - How to verify your details
• **Interview Schedule** - Oral and Written test dates
• **Marks Entry** - Where to check test scores
• **Status Tracking** - Application and Admission status
• **Complete Process** - Full step-by-step guide
• **Reports** - Available reports and downloads
• **Fees** - Payment information

What would you like to know about? Or tell me what stage you've completed!""",
            "category": "help",
            "confidence": 0.5,
            "intent": "general_help"
}
chatbot = ChatbotEngine()
# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "active",
        "service": "IVRM Pre-Admission Chatbot",
        "version": "2.0.0",
        "technology": "Python Flask",
        "features": [
            "Application Form guidance",
            "Health Form instructions",
            "Registration & Document View",
            "Interview Scheduling (Oral & Written)",
            "Marks Entry information",
            "Status Tracking (Application & Admission)",
            "Transfer Student process",
            "Reports Module (5 types)",
            "Fees information"
        ],
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chatbot/greeting', methods=['GET'])
def get_greeting():
    return jsonify({
        "message": "Hi! I'm your intelligent pre-admission assistant. Ask me anything about the admission process!",
        "suggested_questions": [
            "How will I know if my child is selected?",
            "What to do after attending the interview?",
            "Where can I check test marks?",
            "How do I fill the application form?",
            "Show me the complete admission process"
        ],
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chatbot/message', methods=['POST'])
def process_message():
    """Main chat endpoint - process user message and return response"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            "error": "Message is required",
            "timestamp": datetime.now().isoformat()
        }), 400
    
    user_message = data.get('message', '')
    session_id = data.get('sessionId')
    user_id = data.get('userId')
    conversation_history = data.get('conversationHistory', [])
    
    # Get response from chatbot engine WITH CONTEXT
    result = chatbot.find_best_response(user_message, conversation_history)
    
    return jsonify({
        "user_message": user_message,
        "bot_response": result["response"],
        "category": result["category"],
        "confidence": result.get("confidence", 0),
        "matched_keywords": result.get("matched_keywords", []),
        "intent": result.get("intent"),
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chatbot/topics', methods=['GET'])
def get_topics():
    """Get all available topics"""
    topics = []
    for key, data in KNOWLEDGE_BASE.items():
        topics.append({
            "id": key,
            "name": re.sub(r'([A-Z])', r' \1', key).strip().title(),
            "keywords": data["keywords"],
            "response_count": len(data["responses"])
        })
    
    return jsonify({
        "topics": topics,
        "count": len(topics),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chatbot/help/<topic>', methods=['GET'])
def get_topic_help(topic):
    """Get help for a specific topic"""
    if topic in KNOWLEDGE_BASE:
        return jsonify({
            "topic": topic,
            "responses": KNOWLEDGE_BASE[topic]["responses"],
            "keywords": KNOWLEDGE_BASE[topic]["keywords"],
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({
            "error": "Topic not found",
            "available_topics": list(KNOWLEDGE_BASE.keys()),
            "timestamp": datetime.now().isoformat()
        }), 404


@app.route('/api/chatbot/process-flow', methods=['GET'])
def get_process_flow():
    """Get complete admission process flow"""
    return jsonify({
        "process_flow": [
            {
                "step": 1,
                "name": "Fill Application Form",
                "description": "Complete student and parent details, upload photo and necessary documents."
            },
            {
                "step": 2,
                "name": "Fill Health Form",
                "description": "Provide health details, chronic conditions, preferred hospital, and emergency contact. This is mandatory."
            },
            {
                "step": 3,
                "name": "Verify in Registration Page",
                "description": "Review all entered information in the Registration page and correct any errors before final submission."
            },
            {
                "step": 4,
                "name": "Interview Scheduling",
                "description": "School assigns Oral and Written test dates. Check Interview Schedule for date, time and venue."
            },
            {
                "step": 5,
                "name": "Attend Tests",
                "description": "Attend Oral and Written tests as scheduled; bring necessary documents and admit card if provided."
            },
            {
                "step": 6,
                "name": "Marks Entry",
                "description": "School uploads oral and written test marks in the Marks Entry section after evaluating tests."
            },
            {
                "step": 7,
                "name": "Monitor Application Status",
                "description": "Track Application Status (Waiting / Rejected / Accepted) in the Preadmission Status page."
            },
            {
                "step": 8,
                "name": "Monitor Admission Status",
                "description": "After acceptance, Admission Status shows In Progress → Selected → Confirmed."
            },
            {
                "step": 9,
                "name": "Transfer to Admission",
                "description": "Once Confirmed, student appears in Transfer Pre Admission to Admission. Admin finalises enrollment."
            },
            {
                "step": 10,
                "name": "Reports & Documentation",
                "description": "Generate/download necessary reports (Prospectus, Registration, Schedule, Enquiry, Student Count) and fee receipts."
            }
        ],
        "timestamp": datetime.now().isoformat()
    })


# Health-check / root quick page (optional friendly text)
@app.route('/', methods=['GET'])
def root_page():
    return (
        "<h3>IVRM Pre-Admission Chatbot API</h3>"
        "<p>Use <code>/api/chatbot/message</code> POST to talk to the bot. "
        "See <code>/api/health</code> and <code>/api/chatbot/greeting</code>.</p>"
    )
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    user_message = data.get("message", "")

    engine = ChatbotEngine()
    result = engine.detect_intent(user_message)

    if result:
        return jsonify({"response": result["response"]})

    # fallback: keyword-based search
    for key, item in KNOWLEDGE_BASE.items():
        if any(kw in user_message.lower() for kw in item["keywords"]):
            return jsonify({"response": random.choice(item["responses"])})

    return jsonify({"response": "I couldn't understand that. Can you rephrase?"})






if __name__ == "__main__":
    app.run(debug=True, port=5000)