$('.plus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[1]
    console.log('this is plus cart'),

    $.ajax({
        type : 'GET',
        url : '/pluscart',

        data : {
            prod_id : id
            
        },
        error: function(error){
            console.error(error);
        }
    })

})

$('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[1]
    $.ajax({
        type : 'GET',
        url : 'minuscart',
        data : {
            prod_id : id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount

        },
        error: function(error){
            console.error(error);
        }
    })

})