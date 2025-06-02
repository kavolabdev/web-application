let socket;

$(document).ready(function () {
  

  $('#sendBtn').click(async function () {

      try {

        const message = $('#dataInput').val();
        console.log(message);

        const hexArray = message.split(" ");
        console.log(hexArray.length);
        const bufferToSend = [];
        
       for (const h of hexArray) {
          const byte = parseInt(h, 16);
          bufferToSend.push(byte);
        }

        const port = await navigator.serial.requestPort();

        const opts = {
          baudRate: 57600,
          dataBits: 8,
          parity: "none",
          stopBits: 1,
          flowControl: "none"
        }
        await port.open(opts);
        console.log("port opened");

      } catch (err) {
        console.error("serial port error:", err);
      }
  

  })



});