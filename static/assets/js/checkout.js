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
console.log(csrfmiddlewaretoken);
            // console.log(name,number,email)
     // console.log(name, number, email)


     var data
$.ajax({
    method: "GET",
    url: "/proceed_to_pay",
    success: function(response) {
        console.log(response);
        const orderId = response.order_id
        const totalAmount = response.total_price
        const csrf_token = csrfmiddlewaretoken
        console.log('1', response,orderId);
        var options = {
            "key": "rzp_test_PCJ9PYp4rFSfTh",
            "amount": response.total_price * 100,
            "currency": "INR",
            "name": "Fruitkha",
            "description": "Thank You For Buying From Us",
            "image": "assets/img/favicon.png",
            "order_id": response.temp,
            "handler": function(response) {
                console.log('2', response.total_price);
                // alert(response.total_price);
                console.log(options);
                 data = {
                    "payment_id": response.razorpay_payment_id,
                    "order_id":orderId,
                    "total": totalAmount,
                    "csrfmiddlewaretoken": csrf_token
                };
                console.log(data, 'here that change');
                $.ajax({
                    type: "POST",
                    url: "/online_order",
                    data: data,
                    success: function(responsec) {
                        alert(responsec.status);
                        window.location.href = "/succes";
                    }
                });
                console.log(name, email, number);
            },

            "prefill": {
                "name": name, // assuming name, email, and number are correctly populated
                "email": email,
                "contact": '9898989898' // assuming number is correctly populated
            },
            "theme": {
                "color": "#3399cc"
            }

        };
        var rzp1 = new Razorpay(options);
        rzp1.open();

        rzp1.on('payment.failed', function(response) {
            data={
                "order_id":orderId,
                "total":totalAmount,
                "csrfmiddlewaretoken":csrf_token
            }
            console.log("data:", data);
            fetch("/failed_order", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token 
                },
                
                body: JSON.stringify(data)
            })
            .then(response=>response.json)
            .then(data=>{
                // Swal.fire({
                //     icon: 'error',
                //     title: 'Payment Failed',
                //     text: 'Oops! Something went wrong with your payment. Please try again.',
                //     confirmButtonText: 'OK',
                // })
                alert("Payment Failed")
                window.location.reload('/shop')
                
            })
        });
    }
});

            
        });
    });



