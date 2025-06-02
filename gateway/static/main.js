let socket;

$(document).ready(function () {
  
  $.get('/ports', function (ports) {
    ports.forEach(p => {
      $('#ports').append(`<option value="${p}">${p}</option>`);
    });
  });

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

        const info = selectedPort.getInfo();
        let displayName = "Port selected.";
        if (info.usbVendorId && info.usbProductId) {
        displayName += ` USB Vendor: 0x${info.usbVendorId.toString(16)}, Product: 0x${info.usbProductId.toString(16)}`;
        } else {
        displayName += " (No USB info)";
        }

        $('#selectedPortInfo').text(displayName);


        const opts = {
          baudRate: 57600,
          dataBits: 8,
          parity: "none",
          stopBits: 1,
          flowControl: "none"
        }
        await port.open(opts);
        console.log("port opened");
        
        const writer = port.writable.getWriter();
        await writer.write(new Uint8Array(bufferToSend));
        writer.releaseLock();

        console.log("Data sent. Waiting to read...");
        const reader = port.readable.getReader();
        const output = $('#receivedOutput');
        let fullResponse = [];

        console.log("Reading data...");
        let totalBytesRead = 0;
        const maxBytes = 60;
        while (totalBytesRead < maxBytes) {
          const { value, done } = await reader.read();
          if (done) {
            break;
          }
          if (value && value.length > 0) {
            const remaining = maxBytes - totalBytesRead;
            const slice = value.slice(0, remaining);
            fullResponse.push(...slice);
            totalBytesRead += slice.length;
          }
        }

        reader.releaseLock();
        await port.close();

        const hexString = fullResponse.map(b => b.toString(16).padStart(2, '0')).join(' ');
        console.log("Total Bytes Received:", totalBytesRead);
        console.log("Hex String:", hexString);
        output.text(hexString);


      } catch (err) {
        console.error("serial port error:", err);
      }
  

  })



});