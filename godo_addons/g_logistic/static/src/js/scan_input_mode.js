 $(function() {
     var search_text = $("input[name='search_text']")
     console.log(search_text)

     search_text.on("keydown", function(event) {
         if (event.which == 13) {
             let code_arr = search_text.val() // $("input[name='search_text']").val()
             code_item = code_arr[3]
             console.log(code_item)

             search_text.blur()

             setTimeout(() => {
                 search_text.val('')
                 search_text.focus().select()
             }, 10)
         }
     })

 });