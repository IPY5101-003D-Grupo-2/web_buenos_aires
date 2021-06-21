$(document).ready(()=>{
$("#btnConfirmarCompra").click((e) => {
    console.log(e);
    const $fields = $(
      "#full_name, #card_number, #cvv_number, #type, #expiration_month, #expiration_year"
    );

    function allFilled(fields) {
      return (
        fields.filter(function () {
          return this.value === "";
        }).length == 0
      );
    }
    if (allFilled($fields)) {
      e.preventDefault();
      swal({
        title: "Validar medio de pago",
        text: "¿Está seguro de realizar esta acción?",
        icon: "warning",
        buttons: {
          cancel: {
            text: "Cancelar",
            value: null,
            visible: true,
            className: "",
            closeModal: true,
          },
          confirm: {
            text: "Validar",
            value: true,
            visible: true,
            className: "",
            closeModal: false,
          },
        },
      }).then((value) => {
        if (!value) return;
        fetch("/ventas/comprobar-medio-de-pago/", {
          method: "POST",
          body: JSON.stringify({
            full_name: $("#full_name").val(),
            card_number: Number($("#card_number").val()),
            cvv_number: Number($("#cvv_number").val()),
            type: $("#type").val(),
            expiration_month: Number($("#expiration_month").val()),
            expiration_year: Number($("#expiration_year").val()),
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
            console.log(result);
            if (result.ok) {
              // eslint-disable-next-line no-undef
              swal(
                "¡Validada!",
                "Tu tarjeta ha sido validada exitosamente.",
                "success"
              );
            }
            else{
              swal(
                "¡Error!",
                "Tu tarjeta no es válida, reingresa tus datos de pago.",
                "warning"
              );
            }
          });
      });
  };

})})