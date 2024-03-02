$(document).ready(function () {
    $('#rzp-button1').click(function (e) { 
        e.preventDefault();

        // Updating the HTML content to input fields
        $("#name").html('<input type="text" name="name" value="' + $("#name").text() + '">');
        $("#number").html('<input type="text" name="number" value="' + $("#number").text() + '">');
        $("#email").html('<input type="text" name="email" value="' + $("#email").text() + '">');
        $("#house_name").html('<input type="text" name="house_name" value="' + $("#house_name").text() + '">');
        $("#post").html('<input type="text" name="post" value="' + $("#post").text() + '">');
        $("#state").html('<input type="text" name="state" value="' + $("#state").text() + '">');
        $("#pincode").html('<input type="text" name="pincode" value="' + $("#pincode").text() + '">');
        $("#csrfmiddlewaretoken").html('<input type="text" name="csrfmiddlewaretoken" value="' + $("#csrfmiddlewaretoken").text() + '">');
        
        // Retrieving the updated values
        var name = $("input[name='name']").val();
        var number = $("input[name='number']").val();
        var email = $("input[name='email']").val();
        var house_name = $("input[name='house_name']").val();
        var post = $("input[name='post']").val();
        var state = $("input[name='state']").val();
        var pincode = $("input[name='pincode']").val();
        var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        // console.log(name,number,email)
        $.ajax({
            method: "GET",
            url: "/proceed_to_pay",
            success: function (response) {
                console.log('1',response);
                var options = {
                    "key": "rzp_test_PCJ9PYp4rFSfTh",
                    "amount": response.total_price*100 , 
                    "currency": "INR",
                    "name": "Fruitkha", 
                    "description": "Thak You For Buying From As",
                    "image": "assets/img/favicon.png",
                    "order_id": response.temp,
                    "handler": function (responseb){
                        console.log('2',response);
                        alert(responseb.razorpay_payment_id);
                        console.log(options)
                        data = {
                            "payment_id" : responseb.razorpay_payment_id,
                            "order_id" : response.order_id,
                            "total" :response.total_price,
                            csrfmiddlewaretoken:csrfmiddlewaretoken
                        }
                        $.ajax({
                            type: "POST",
                            url: "/online_order/",
                            data: data,
                            success: function (responsec) {
                                alert(responsec.status)
                                window.location.href = "/succes";
                                
                            }
                        });console.log(name,email,number);
                    },
                    
                    "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        "name": name, //your customer's name
                        "email": email, 
                        "contact": 9898989898  //Provide the customer's phone number for better conversion rates 
                        
                    },
                    // "notes": {
                    //     "address": "Razorpay Corporate Office"
                    // },
                    "theme": {
                        "color": "#3399cc"
                    }
                    
                };
                var rzp1 = new Razorpay(options)
                console.log('3',response.temp);
               rzp1.open();
            }
        });
        
    });
});