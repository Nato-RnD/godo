odoo.define('g_logistic.scan_mode', function(require) {
    console.log('Da khai bao roi')
    var search_text = $("input[name='search_text']")
    console.log(search_text)

    search_text.addEventListener("keydown", function(event) {
        if (event.which == 13) {
            let code_arr = $("input[name='search_text']").val()
            code_item = code_arr[3]
            console.log(code_item)

            $("input[name='search_text']").focusout()

            // console.log("code",code_item)
            // $.ajax({
            //     url: `/api/get-product-tracebility-by-code`,
            //     type: "GET",
            //     data: {
            //         'code': code_item
            //     },

            //     success: function(res) {
            //         var data = JSON.parse(res)
            //             // console.log("traceability_id",data.data)
            //         if (data.status == true) {
            //             var api = {
            //                 "list_price": data.data['price'] != null || data.data['price'] && data.data['price'].length > 0 ? data.data['price'] : 0,
            //                 "name": data.data['name'] != null || data.data['name'] && data.data['name'].length > 0 ? data.data['name'] : '',
            //                 "image_medium": data.data['image'] != null || data.data['image'] && data.data['image'].length > 0 ? data.data['image'] : '',
            //                 "traceability_id": data.data['product_id'] != null || data.data['product_id'] && data.data['product_id'].length > 0 ? data.data['product_id'] : 0,
            //             }
            //         } else {
            //             window.alert(data.message)
            //         }

            //         event.preventDefault();
            //         $('div[name="list_price"] :input').val(api['list_price']);
            //         for (key in api) {
            //             if (api.hasOwnProperty(key))
            //                 $('input[name=' + key + ']').val(api[key]);
            //         }
            //         setTimeout(function() {
            //             $("input[name='traceability_id']").focus().select()
            //         }, 10)
            //     },
            //     error: function(xhr) {
            //         setTimeout(function() {
            //             $("input[name='traceability_id']").focus().select()
            //         }, 10)
            //     }
            // })
        }
    })

});