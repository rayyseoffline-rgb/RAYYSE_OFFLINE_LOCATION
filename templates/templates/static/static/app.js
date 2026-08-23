function getLocation(){

    let status = document.getElementById("status");

    status.innerHTML = "📡 در حال اتصال به GPS...";

    if (navigator.geolocation){

        navigator.geolocation.getCurrentPosition(

        function(position){

            let latitude = position.coords.latitude;
            let longitude = position.coords.longitude;


            fetch("/send_location",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    lat: latitude,
                    lng: longitude

                })

            })

            .then(()=>{

                status.innerHTML =
                "✅ موقعیت با موفقیت ارسال شد";

            });


        },


        function(){

            status.innerHTML =
            "❌ اجازه موقعیت داده نشد";

        });


    }

    else{

        status.innerHTML =
        "مرورگر شما GPS را پشتیبانی نمی‌کند";

    }

}
