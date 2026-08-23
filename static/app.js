console.log("⚡ RAYYSE OFFLINE SYSTEM STARTED");


function getLocation(){

    let result = document.getElementById("result");

    result.innerHTML =
    "📡 Connecting to system...";


    if(navigator.geolocation){


        navigator.geolocation.getCurrentPosition(

        function(position){


            let lat =
            position.coords.latitude;


            let lng =
            position.coords.longitude;


            result.innerHTML =
            "✅ Location Ready<br>" +
            "LAT: " + lat +
            "<br>" +
            "LNG: " + lng;


            fetch("/send_location",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    lat:lat,
                    lng:lng

                })

            });


        },


        function(){

            result.innerHTML =
            "❌ Location permission denied";

        });


    }

    else{

        result.innerHTML =
        "Browser does not support location";

    }

}
