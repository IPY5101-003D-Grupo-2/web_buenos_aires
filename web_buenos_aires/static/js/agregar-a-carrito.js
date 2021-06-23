$(document).ready(()=>{
    $(".agregar-al-carro").click((e) => {
        const idBtn = e.currentTarget.id
        const sku = $(`#${idBtn}`).data('sku')
        const cantidad = $(`#cantidad-${idBtn.split('-')[2]}`).val()
        const $fields = $(
          idBtn, `#cantidad-${idBtn.split('-')[2]}`
        );
    
        function allFilled(fields) {
          return (
            fields.filter(function () {
              return this.value === "";
            }).length == 0
          );
        }
        console.log(sku)
        if (allFilled($fields)) {
          e.preventDefault();
        //   swal({
        //     title: "Validar medio de pago",
        //     text: "¿Está seguro de realizar esta acción?",
        //     icon: "warning",
        //     buttons: {
        //       cancel: {
        //         text: "Cancelar",
        //         value: null,
        //         visible: true,
        //         className: "",
        //         closeModal: true,
        //       },
        //       confirm: {
        //         text: "Validar",
        //         value: true,
        //         visible: true,
        //         className: "",
        //         closeModal: false,
        //       },
        //     },
        //   }).then((value) => {
        //     if (!value) return;
            fetch("/ventas/agregar-a-carrito/", {
              method: "POST",
              body: JSON.stringify({
                sku: sku,
                cantidad: Number($(`#cantidad-${idBtn.split('-')[2]}`).val()),
              }),
              headers: {
                "content-type": "application/json",
                // eslint-disable-next-line no-undef
                "X-CSRFToken": csrftoken,
              },
            })
              .then(async (response) => {
                if (response.status === 400) {
                  swal(
                    "Cancelado",
                    "No se ha podido completar su solicitud, inténtelo en unos momentos",
                    "error"
                  );
                }
    
                return response;
              })
              .then(async (result) => {
                if (result.ok) {
                  // eslint-disable-next-line no-undef
                  swal(
                    "¡Agregado!",
                    "Tu producto a sido agregado al carrito exitosamente.",
                    "success"
                  ).then(()=>{
                      location.reload();
                  })
                }
                else{
                  swal(
                    "¡Error!",
                    "No hemos podido agregar tu producto al carro, reintentalo en unos minutos.",
                    "warning"
                  );
                }
              });
        //   });
      };
    
    })}
    )