function sortList(element) 
{ 
    var lb = document.getElementById(element); 
    arrTexts = new Array(); 
    arrValues = new Array(); 
    arrOldTexts = new Array(); 

    for(i=0; i<lb.length; i++) 
    { 
        arrTexts[i] = lb.options[i].text; 
        arrValues[i] = lb.options[i].value; 
        arrOldTexts[i] = lb.options[i].text; 
    } 

    arrTexts.sort(); 

    for(i=0; i<lb.length; i++) 
    { 
        lb.options[i].text = arrTexts[i]; 
        for(j=0; j<lb.length; j++) 
        { 
            if (arrTexts[i] == arrOldTexts[j]) 
            { 
                lb.options[i].value = arrValues[j]; 
                j = lb.length; 
            } 
        } 
    } 
}