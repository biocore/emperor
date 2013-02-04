function showAbout()
{
    document.getElementById("about").className = "visible";
    document.getElementById("screenshots").className = "hidden";
    document.getElementById("tutorial").className = "hidden";
    
}

function showScreenshots()
{
    document.getElementById("about").className = "hidden";
    document.getElementById("screenshots").className = "visible";
    document.getElementById("tutorial").className = "hidden";
    
}

function showTutorial()
{
    document.getElementById("about").className = "hidden";
    document.getElementById("screenshots").className = "hidden";
    document.getElementById("tutorial").className = "visible";
    
}