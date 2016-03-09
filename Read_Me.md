MedMinder (c) 2016
=============
##Author: Patricia Arbona
#####<i>A Hackbright Academy Capstone Project
<b>Tech Stack</b>: Python, Flask, SQLAlchemy Postgresql, Bootstrap 3, Python DateTime Library, Flask Mail, Jinja2
Feel free to reach me at:
<li><a href="https://www.linkedin.com/in/parbona">LinkedIn</a></li>
<li>arbonap@gmail.com</li>


<b>MedMinder</b>
<br>
Have you ever struggled to remember to take your medication during a busy day? 
Have you ever missed a doctor's appointment because it slipped your mind? 
MedMinder was created to alleviate this challenge. 
MedMinder is a reminder web-app that dynamically displays a user's personalized health information, 
empowering patients to take control of their healthcare. 
Your health should never be negatively impacted by missed doses due to complicated dosage schedules. 
MedMinder notifies the user's upcoming prescription doses and future medical appointments, 
both within the app itself and also via email.

####Here the user submits their prescription information:
![Prescription Registration](https://github.com/arbonap/medicine-final-project/blob/master/static/Screen%20Shot%202016-03-08%20at%205.59.41%20PM.png "Registering User Medicines")

####After submitting their prescription information, the user is brought to the Prescription Dashboard:
![Prescription Dashboard](https://github.com/arbonap/medicine-final-project/blob/master/static/Screen%20Shot%202016-03-08%20at%206.00.26%20PM.png "User's Prescription Dashboard")
 * Here the user sees their upcoming scheduled medication schedule for each prescription
 * The user has an option toward the bottom of the page to email themselves their prescription schedule
 
####When the user navigates to the homepage, the user is reminded to take their medication if they look at the homepage within one hour before their medication is scheduled to be taken:
![Medication reminder from within app one hour before medication needs to be taken](https://github.com/arbonap/medicine-final-project/blob/master/static/Screen%20Shot%202016-03-08%20at%206.00.48%20PM.png "One-hour reminder within MedMinder to take prescription")

####Here the user submits information about upcoming medical appointments:
![Medical Appointment Registration form](https://github.com/arbonap/medicine-final-project/blob/master/static/Screen%20Shot%202016-03-08%20at%206.01.05%20PM.png "Medical Appointments Registration Form"]
  * It is vital for users who have many medical appointments to be able to have a dashboard that displays all of their appointments in one, easy-to-find place

####This is the Doctor's Appointments Dashboard:
![Upcoming Medical Appointments Dashboard](https://github.com/arbonap/medicine-final-project/blob/master/static/Screen%20Shot%202016-03-08%20at%206.01.18%20PM.png "Upcoming Medical Appointments Dashboard")

####Version 2.0 of MedMinder:
 * I would love to hash and salt my databases' usernames and passwords to heighten users' privacy
 * I will definitely reasearch and utilize Python's Celery, a task queue; it communicates via messages, utilizing a broker to mediate between cients and workers.

 

