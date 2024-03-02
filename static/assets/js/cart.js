$(document).ready(function(){
    $('#cart1').on('click','.chenge_quantity',function(e){
        e.preventDefault()
        var products_id = $(this).data('product-id')
        var action = $(this).data('action')
        var token = $('input[name=csrfmiddlewaretoken]').val()

        $.ajax({
            method: 'POST',
            url : 'quantity_cart',
            data : {
                products_id: products_id,
                action: action,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // $('#cart').load('cart_page')
                if (response.status) {
                    console.log('succes')
                  $('#cart1').load('/cart_page #cart')
                  
                }
              },
              error: (error) => {
                console.log(error)
              }
        })
        
    })
})



// $(document).ready(function () {
//     $('#reload').on('click', '.change_quantity', function (e) {
//       e.preventDefault()
  
//       var products_id = $(this).data('product-id')
  
//       var token = $('input[name=csrfmiddlewaretoken]').val()
  
//       var action = $(this).data('action')
//       $.ajax({
//         method: 'POST',
//         url: '/change_quantity/',
//         data: {
//           products_id: products_id,
  
//           action: action,
//           csrfmiddlewaretoken: token
//         },
  
//         success: function (response) {
//           if (response.status) {
//             $('#reload').load('/cart/ #reload')
//             $('#2load').load('/cart/ #2load')
//           }
//         },
//         error: (error) => {
//           console.log(error)
//         }
//       })
//     })
//   })