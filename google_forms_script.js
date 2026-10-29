/**
 * GOOGLE FORMS AUTO-GENERATOR SCRIPT FOR FLEXIFIT (IST2106) - FIXED & TESTED
 * 
 * 1. Go to: https://script.google.com
 * 2. Paste this entire code into Code.gs (replacing whatever is there).
 * 3. Click the Save icon, then click "Run".
 * 4. In the Execution log below, it will print your live Google Form link!
 */

function createFlexiFitSurvey() {
  const form = FormApp.create('FlexiFit: Urban Fitness & Lifestyle Habits Survey (Kampala)');
  
  form.setDescription(
    'Academic Field Research — IST2106: Technopreneurship & Digital Marketing\n\n' +
    'Study Objective: To evaluate daily exercise routines, local nutrition tracking habits, and remote personal coaching dynamics among urban residents in Kampala.\n\n' +
    'Target Participants: Urban Adults & Fitness Enthusiasts\n' +
    'Time to complete: ~3-4 minutes\n' +
    'Privacy: All responses are completely anonymous and used for academic coursework only.'
  );
  
  form.setConfirmationMessage('Thank you for completing the survey! Your responses directly inform our Technopreneurship capstone venture (FlexiFit).');

  // ================= SECTION A =================
  form.addSectionHeaderItem()
    .setTitle('SECTION A: Demographic Profile')
    .setHelpText('Basic demographic background.');

  // Q1
  form.addMultipleChoiceItem()
    .setTitle('1. Age Group:')
    .setChoiceValues(['18-24 years', '25-34 years', '35-44 years', '45+ years'])
    .setRequired(true);

  // Q2
  form.addMultipleChoiceItem()
    .setTitle('2. Current Primary Occupation:')
    .setChoiceValues([
      'Corporate / Office Employee',
      'Business Owner / Self-Employed',
      'University / Tertiary Student',
      'Other'
    ])
    .setRequired(true);

  // Q3
  form.addMultipleChoiceItem()
    .setTitle('3. How frequently do you currently engage in physical exercise?')
    .setChoiceValues([
      'Rarely / Never',
      '1-2 times per week',
      '3-4 times per week',
      '5+ times per week'
    ])
    .setRequired(true);

  // ================= SECTION B =================
  form.addSectionHeaderItem()
    .setTitle('SECTION B: Exercise Habits & Preferred Workout Environments')
    .setHelpText('Understanding where and why you work out.');

  // Q4
  form.addMultipleChoiceItem()
    .setTitle('4. Where do you currently perform most of your physical workouts?')
    .setChoiceValues([
      'Commercial Gym Facility',
      'At Home (Living room, compound, balcony)',
      'Outdoor Public Spaces / Estate Roads / Parks',
      'I do not currently exercise'
    ])
    .setRequired(true);

  // Q5
  form.addCheckboxItem()
    .setTitle('5. If you exercise at home or in public spaces rather than a gym, what are your MAIN reasons? (Select up to 2)')
    .setChoiceValues([
      'High cost of commercial gym memberships',
      'Commute time and severe evening traffic jams',
      'Overcrowded facilities & waiting for equipment',
      'Privacy concerns / gym intimidation in public spaces',
      'Schedule flexibility to workout whenever free'
    ]);

  // Q6
  form.addMultipleChoiceItem()
    .setTitle('6. What is your biggest frustration when exercising independently without a trainer present?')
    .setChoiceValues([
      'Difficulty staying consistent and motivated',
      'Lack of a structured routine to follow',
      'Uncertainty about proper exercise technique/form',
      'Not seeing visible progress or results'
    ])
    .setRequired(true);

  // ================= SECTION C =================
  form.addSectionHeaderItem()
    .setTitle('SECTION C: Meal Planning & Local Diet Challenges')
    .setHelpText('Evaluating nutritional habits with East African foods.');

  // Q7
  form.addMultipleChoiceItem()
    .setTitle('7. How do you currently manage your daily diet and meal choices?')
    .setChoiceValues([
      'Follow a structured diet plan',
      'Try to eat healthy informally without precise tracking',
      'I do not track my food intake at all'
    ])
    .setRequired(true);

  // Q8
  form.addMultipleChoiceItem()
    .setTitle('8. Have you ever used mobile health or meal tracking applications in the past (e.g. MyFitnessPal)?')
    .setChoiceValues([
      'Yes, currently use them',
      'Used previously but stopped',
      'Never used them'
    ])
    .setRequired(true);

  // Q9
  form.addCheckboxItem()
    .setTitle('9. If you stopped using or avoid diet apps, what were the main drawbacks? (Select top 2)')
    .setChoiceValues([
      'App did not include Ugandan foods (Matooke, Posho, Cassava, Beans, G-nuts)',
      'Recommended recipes required expensive or unavailable foreign ingredients',
      'Logging meals manually took too much time and effort',
      'Not applicable'
    ]);

  // Q10
  form.addMultipleChoiceItem()
    .setTitle('10. How helpful would it be to have a diet plan built specifically around affordable, locally available staple foods?')
    .setChoiceValues([
      'Extremely Helpful',
      'Moderately Helpful',
      'Slightly Helpful',
      'Not Helpful At All'
    ])
    .setRequired(true);

  // ================= SECTION D =================
  form.addSectionHeaderItem()
    .setTitle('SECTION D: Personal Training & Coaching Preferences')
    .setHelpText('Evaluating accountability and trainer interaction.');

  // Q11
  form.addMultipleChoiceItem()
    .setTitle('11. When working with a fitness instructor, which coaching structure do you prefer?')
    .setChoiceValues([
      'An instructor standing next to me in-person during every single physical workout session',
      'A qualified instructor who designs my weekly workout & local meal routine, checking my progress and form periodically without needing to stand beside me daily'
    ])
    .setRequired(true);

  // Q12
  form.addMultipleChoiceItem()
    .setTitle('12. How do you currently communicate with or receive guidance from fitness instructors or nutritionists?')
    .setChoiceValues([
      'In-person sessions at a gym',
      'Informal WhatsApp / text messaging',
      'Social media (Instagram / TikTok videos)',
      'I do not currently consult a coach/nutritionist'
    ])
    .setRequired(true);

  // Q13
  form.addCheckboxItem()
    .setTitle('13. What form of ongoing support is most effective for keeping you accountable? (Select top 2)')
    .setChoiceValues([
      'Having a customized weekly meal and exercise schedule',
      'Receiving periodic feedback on exercise form and progress metrics',
      'Having direct messaging/WhatsApp access to ask questions when needed',
      'In-person live supervision during workouts'
    ]);

  // ================= SECTION E (UGX CURRENCY) =================
  form.addSectionHeaderItem()
    .setTitle('SECTION E: Fitness Expenditure & Service Value (Uganda Shillings — UGX)')
    .setHelpText('Evaluating current spending and willingness-to-pay in local currency.');

  // Q14 (UGX)
  form.addMultipleChoiceItem()
    .setTitle('14. Approximately how much do you currently spend per month on gym memberships, trainer services, or fitness activities?')
    .setChoiceValues([
      'UGX 0 / Nothing (I work out for free or do not exercise)',
      'Under UGX 50,000 / month (Occasional day passes, basic gear)',
      'UGX 50,000 - UGX 150,000 / month (Standard neighborhood gym)',
      'UGX 150,000 - UGX 300,000 / month (Mid-tier commercial gym membership)',
      'Over UGX 300,000 / month (Premium health club or personal trainer)'
    ])
    .setRequired(true);

  // Q15 (UGX)
  form.addMultipleChoiceItem()
    .setTitle('15. If a professional service provided you with a certified trainer who customized your weekly workouts, designed meals using affordable Ugandan foods, and tracked your progress remotely, what monthly subscription feels fair?')
    .setChoiceValues([
      'Under UGX 30,000 / month',
      'UGX 30,000 - UGX 50,000 / month (Budget-friendly)',
      'UGX 50,000 - UGX 80,000 / month (Standard recommended tier)',
      'UGX 80,000 - UGX 120,000 / month (Premium tier with video calls)',
      'Over UGX 120,000 / month'
    ])
    .setRequired(true);

  // Q16
  form.addParagraphTextItem()
    .setTitle('16. Any additional thoughts on what prevents you from achieving your ideal fitness goals in Kampala?')
    .setHelpText('Optional comments on traffic, work schedules, canteen food, etc.')
    .setRequired(false);

  // Log URLs
  const liveUrl = form.getPublishedUrl();
  const editUrl = form.getEditUrl();
  
  Logger.log('==============================================');
  Logger.log('SUCCESS! YOUR FORM IS READY:');
  Logger.log('LIVE SHAREABLE FORM LINK (for WhatsApp):');
  Logger.log(liveUrl);
  Logger.log('EDIT / RESPONSES LINK:');
  Logger.log(editUrl);
  Logger.log('==============================================');
}
