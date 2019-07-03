export const translateName = (name: string): string => {
    const replacements = {
        "St$": "State",
        "St\\.": "Saint",
        "Prairie View A&M": "Prairie View",
        "\\(pa\\)": "(PA)",
        "North Carolina$": "UNC",
        "Ucf$": "UCF",
        "Saint John's$": "St. John's (NY)",
        "UC Irvine$": "UC-Irvine",
        "Liu Brooklyn$": "LIU-Brooklyn",
        "East Tennessee State$": "ETSU",
        "Charleston$": "College of Charleston",
        "UT Arlington$": "Texas-Arlington"
    }
    
    
    Object.keys(replacements).forEach(r => {
        const regex = new RegExp(r, "gm") 
        if(name.match(regex)){
            // console.log(`Found ${r} in name. Replacing. ${regex}`)
            name = name.replace(regex, replacements[r])
        }
    })
	return name;
};
