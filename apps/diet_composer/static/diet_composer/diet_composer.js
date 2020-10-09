$("#id_category").change(function () {
      var url = $("#product-form").attr("data-products-url");  // get the url of the `load_products` view
      var categoryId = $(this).val();  // get the selected category ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load_products/)
        data: {
          'category': categoryId       // add the category id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_product` view function
          $("#id_product").html(data);  // replace the contents of the product input with the data that came from the server
        }
      });

    });