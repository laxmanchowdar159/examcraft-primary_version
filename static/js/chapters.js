const chaptersBySubject = {
  "Maths": [
    "Real Numbers",
    "Polynomials",
    "Pair of Linear Equations in Two Variables",
    "Quadratic Equations",
    "Arithmetic Progressions",
    "Triangles",
    "Coordinate Geometry",
    "Introduction to Trigonometry",
    "Some Applications of Trigonometry",
    "Circles",
    "Constructions",
    "Areas Related to Circles",
    "Surface Areas and Volumes",
    "Statistics",
    "Probability"
  ],

  "Science": [
    "Chemical Reactions and Equations",
    "Acids, Bases, and Salts",
    "Metals and Non-Metals",
    "Carbon and Its Compounds",
    "Periodic Classification of Elements",
    "Life Processes",
    "Control and Coordination",
    "How do Organisms Reproduce?",
    "Heredity and Evolution",
    "Light – Reflection and Refraction",
    "The Human Eye and the Colourful World",
    "Electricity",
    "Magnetic Effects of Electric Current",
    "Sources of Energy"
  ],

  "Social": [
    "Nationalism in India",
    "The Making of a Global World",
    "The Age of Industrialization",
    "Print Culture and the Modern World",
    "Resources and Development",
    "Forest and Wildlife Resources",
    "Water Resources",
    "Agriculture",
    "Minerals and Energy Resources",
    "Manufacturing Industries",
    "Lifelines of National Economy",
    "Power Sharing",
    "Federalism",
    "Democracy and Diversity",
    "Gender, Religion and Caste",
    "Popular Struggles and Movements",
    "Political Parties",
    "Outcomes of Democracy",
    "Challenges to Democracy"
  ],

  "English": [
    "A Letter to God",
    "Nelson Mandela: Long Walk to Freedom",
    "Two Stories about Flying",
    "From the Diary of Anne Frank",
    "Glimpses of India",
    "Mijbil the Otter",
    "Madam Rides the Bus",
    "The Hundred Dresses",
    "The Hundred Dresses – II",
    "A Baker from Goa",
    "Amanda",
    "Animals",
    "The Trees",
    "Fog",
    "The Tale of Custard the Dragon",
    "The Ball Poem",
    "The Invisible Man",
    "The Treasure within",
    "Footprints without Feet",
    "The Magic Drum and Other Favourite Stories",
    "The Necklace",
    "The Hack Driver",
    "Bholi",
    "The Book that Saved the Earth"
  ]
};

document.addEventListener('DOMContentLoaded', () => {
  const subjectSelect = document.getElementById('subject');
  const chapterSelect = document.getElementById('chapter');

  subjectSelect.addEventListener('change', () => {
    const subject = subjectSelect.value;
    chapterSelect.innerHTML = '<option value="" disabled selected>Choose a chapter...</option>';

    if (chaptersBySubject[subject]) {
      chaptersBySubject[subject].forEach(chap => {
        const option = document.createElement('option');
        option.value = chap;
        option.textContent = chap;
        chapterSelect.appendChild(option);
      });
      chapterSelect.disabled = false;
    } else {
      chapterSelect.disabled = true;
    }
  });
});
