function myFunction() {
    //document.getElementById("demo").innerHTML = document.keys;
    

    // use api keys to query current, 1 week ago, 1 month ago AQI against 1 year, 1 year + 1 week, 1 year + 1 month

  }


myFunction();

$(document).ready(function(){
    $("start").click(function(){
        alert("Handler for start called");
        $.ajax({
            url: document.keys["NASA"]["url"],
            type: "GET",
            success: function(result){
                document.getElementById("demo").innerHTML = result
                console.log(result)
            }, 
            error: function(error){
                document.getElementById("demo").innerHTML = error
                console.log(error)
            }
        })
    })
})