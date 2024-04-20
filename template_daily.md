---
rating: "~"
entry_title: Daily note
hidden: false
entry_thumbnail:
---
```dataviewjs
const pg = dv.current();

const entryTitle = pg.entry_title;
const fileName = dv.current().file.name;
const hidden = pg.hidden;
const rating = pg.rating;

if (entryTitle && fileName) {
    // Extract the date from the filename
    const dateParts = fileName.split('-');
    const year = parseInt(dateParts[0]);
    const month = parseInt(dateParts[1]);
    const day = parseInt(dateParts[2]);

    // Check if the extracted values are valid
    if (!isNaN(year) && !isNaN(month) && !isNaN(day)) {
        const date = new Date(year, month - 1, day); // Month is zero-based in JavaScript
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = date.toLocaleDateString('en-UK', options).replace(',', '');

        // Apply background gradient based on month
        let gradientColorStart, gradientColorEnd, textColor, ratingText;
        
        // Set gradient colors based on rating
       if (rating.includes('+++')) {
            ratingText = 'Wonderful';
            gradientColorStart = '#52c234'; // Light green
            gradientColorEnd = '#2f8e0b'; // Dark green
            textColor = 'white'; // White text color
        } else if (rating.includes('++')) {
            ratingText = 'Great';
            gradientColorStart = '#81C784'; // Light green
            gradientColorEnd = '#4CAF50'; // Dark green
            textColor = 'white'; // White text color
        } else if (rating.includes('+') && rating.includes('~')) {
            ratingText = 'Above average';
            gradientColorStart = '#e8f5e9'; // Very light green
            gradientColorEnd = '#c8e6c9'; // Light green
            textColor = 'black'; // Black text color
        } else if (rating.includes('+')) {
            ratingText = 'Good';
            gradientColorStart = '#c5e1a5'; // Light green
            gradientColorEnd = '#aed581'; // Medium green
            textColor = 'black'; // Black text color
        } else if (rating.includes('---')) {
            ratingText = 'Terrible';
            gradientColorStart = '#e57373'; // Light red
            gradientColorEnd = '#d32f2f'; // Dark red
            textColor = 'white'; // White text color
        } else if (rating.includes('--')) {
            ratingText = 'Very bad';
            gradientColorStart = '#ef9a9a'; // Light red
            gradientColorEnd = '#f44336'; // Dark red
            textColor = 'white'; // White text color
        } else if (rating.includes('-') && rating.includes('~')) {
            ratingText = 'Below average';
            gradientColorStart = '#FFEBEE'; // Very light red
            gradientColorEnd = '#9e9e9e'; // Grey
            textColor = 'black'; // Black text color
        } else if (rating.includes('-')) {
            ratingText = 'Bad';
            gradientColorStart = '#ef9a9a'; // Light red
            gradientColorEnd = '#f44336'; // Dark red
            textColor = 'white'; // White text color
        } else if (rating.includes('~')) {
            ratingText = 'Average';
            gradientColorStart = '#cfd8dc'; // Light grey
            gradientColorEnd = '#9e9e9e'; // Grey
            textColor = 'black'; // Black text color
        } else {
            ratingText = 'No rating';
            gradientColorStart = '#cfd8dc'; // Light grey
            gradientColorEnd = '#9e9e9e'; // Grey
            textColor = 'black'; // Black text color
        }

        // Apply gradient background color, rounded corners, and text color to the div
        const headerStyle = `
            display: inline-block;
            background: linear-gradient(to right, white, grey);
            color: black;
            padding: 0;
            border-radius: 10px;
            margin-right: 10px;
            margin-top: 30px;
            margin-bottom: 30px;
            width: 100%;
        `;

        const ratingStyle = `
            display: inline-block;
            background: linear-gradient(to right, ${gradientColorStart}, ${gradientColorEnd});
            color: ${textColor};
            padding: 5px 10px;
            border-radius: 0px 0px 10px 10px;
            margin: 0;
            margin-top: 0px;
            font-size: 28px;
            width: 100%;
        `;

        const lockDiv = hidden ? `<div style="background-color: #f2f2f2; padding: 0px 20px 5px 20px; border-radius: 50px; margin: 10px; display: block; width: fit-content; height: fit-content; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);">
        <span style="font-size: 35px; color: #333; margin: 0; padding: 0;">🔒 Private</span></div>` : '';
        const headerContent = `<div style="${headerStyle}">${lockDiv}<div style="padding: 5px 10px;">${entryTitle}</div><div style="padding: 0px 10px; font-size: 27px; font-weight: lighter;">${formattedDate}</div>
        <br><span style="${ratingStyle}">
         ${ratingText}</span>
        </div>`;

        dv.header(2, "<div style='display: flex; justify-content: space-between;'><a href='obsidian://advanced-uri?vault=Pulvirenti%20Archive&commandid=daily-notes%253Agoto-prev'>← Previous</a> <a href='obsidian://advanced-uri?vault=Pulvirenti%20Archive&commandid=daily-notes%253Agoto-next'>Next →</a></div>");

        dv.header(1, headerContent);

    }
}

```
