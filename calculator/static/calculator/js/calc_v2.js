console.log("calc_v2.js подключен!");
console.log("calc.js версия 20240523-1");
console.log("calc.js загружен, ORDER_ID:", window.ORDER_ID);

// Huawei MateBook E 2023 heuristic detection (robust with resize/orientation)
// Adds/removes 'matebook-e' on <html> so CSS targets only this device
(function () {
  const html = document.documentElement;
  const ua = (navigator.userAgent || "");
  const isWindows = /Windows/i.test(ua);
  const isHuaweiUA = /HUAWEI|MateBook/i.test(ua);
  const isEdge = /Edg\//i.test(ua);
  const qs = new URLSearchParams(window.location.search || "");
  // Persistent manual override using localStorage
  // ?matebook=1 -> enable and persist; ?matebook=0 -> disable and persist
  if (qs.get('matebook') === '1') {
    try { localStorage.setItem('matebook-e', '1'); } catch (_) {}
  } else if (qs.get('matebook') === '0') {
    try { localStorage.setItem('matebook-e', '0'); } catch (_) {}
  }
  let persisted = null;
  try { persisted = localStorage.getItem('matebook-e'); } catch (_) {}
  const manualOverride = qs.has('matebook') || (persisted === '1' || persisted === '0');

  function getViewport() {
    const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    const isLandscape = vw > vh;
    return { vw, vh, isLandscape };
  }

  function looksLikeMateBookNow() {
    const { vw } = getViewport();
    const scrW = (window.screen && screen.width) ? screen.width : vw;
    const hasTouch = (navigator.maxTouchPoints || 0) > 0;
    // Require touch for auto mode so desktops aren't affected
    return (
      hasTouch && (
        (isWindows && (isHuaweiUA || isEdge) && vw >= 992) ||
        (isWindows && scrW >= 992 && scrW <= 2560 && isHuaweiUA)
      )
    );
  }

  let lastApplied = null; // true/false
  function applyClass(shouldEnable) {
    if (shouldEnable) {
      if (!html.classList.contains('matebook-e')) {
        html.classList.add('matebook-e');
        const { vw, vh, isLandscape } = getViewport();
        console.log('matebook-e mode enabled', { ua, vw, vh, isLandscape, touch: navigator.maxTouchPoints });
      }
    } else {
      if (html.classList.contains('matebook-e')) {
        html.classList.remove('matebook-e');
        console.log('matebook-e mode disabled');
      }
    }
    lastApplied = shouldEnable;
  }

  function detectMateBookE() {
    try {
      if (manualOverride) {
        // Apply according to persisted value or query param
        if (qs.get('matebook') === '1' || persisted === '1') {
          console.log('matebook-e manual ON');
          applyClass(true);
          return;
        }
        if (qs.get('matebook') === '0' || persisted === '0') {
          console.log('matebook-e manual OFF');
          applyClass(false);
          return;
        }
      }
      const enable = looksLikeMateBookNow();
      if (enable !== lastApplied) applyClass(enable);
    } catch (e) {
      console.warn('matebook-e detect failed', e);
    }
  }

  // Debounce for resize/orientation changes
  let t = null;
  function debouncedDetect() {
    clearTimeout(t);
    t = setTimeout(detectMateBookE, 150);
  }

  // Initial detect
  detectMateBookE();

  // Re-evaluate on resize/orientation changes
  window.addEventListener('resize', debouncedDetect, { passive: true });
  window.addEventListener('orientationchange', debouncedDetect, { passive: true });
})();

const dateformat = /^(0?[1-9]|[12][0-9]|3[01])[\/\.](0?[1-9]|1[012])[\/\.]\d{4}$/;

    const svgNS = "http://www.w3.org/2000/svg";
    var svg;
    var svgLayer;

    var svg_x = document.getElementById('svg_x');
    var svg_0 = document.getElementById('svg_0');
    var svg_1 = document.getElementById('svg_1');

    var svgLayer_x;
    var svgLayer_0;
    var svgLayer_1;

    /* ------------------------------------------------------------------------- */

    var dotLL0 = [];
    var dotLL20 = [];
    var dotLL40 = [];
    var dotLL60 = [];

    var dotCenter = [];

    var dotLL10 = [];
    var dotLL30 = [];
    var dotLL50 = [];
    var dotLL70 = [];

    var dotMM01 = [];
    var dotMM02 = []; 
    var dotMM21 = [];
    var dotMM22 = [];
    var dotMM41 = [];
    var dotMM42 = [];
    var dotMM61 = [];
    var dotMM62 = [];

    var dotSS11 = [];
    var dotSS12 = [];
    var dotSS13 = [];
    var dotSS51 = [];
    var dotSS52 = [];
    var dotSS53 = [];

    var dotMMC1 = [];
    var dotSSC1 = [];

    var dotXS5 = [];
    var dotXS3 = [];
    var dotXS7 = [];
    var dotXS2 = [];
    var dotXS4 = [];
    var dotXS6 = [];
    var dotXS8 = [];

    var dotXS15 = [];
    var dotXS13 = [];
    var dotXS17 = [];
    var dotXS12 = [];
    var dotXS14 = [];
    var dotXS16 = [];
    var dotXS18 = [];

    var dotXS25 = [];
    var dotXS23 = [];
    var dotXS27 = [];
    var dotXS22 = [];
    var dotXS24 = [];
    var dotXS26 = [];
    var dotXS28 = [];

    var dotXS35 = [];
    var dotXS33 = [];
    var dotXS37 = [];
    var dotXS32 = [];
    var dotXS34 = [];
    var dotXS36 = [];
    var dotXS38 = [];

    var dotXS45 = [];
    var dotXS43 = [];
    var dotXS47 = [];
    var dotXS42 = [];
    var dotXS44 = [];
    var dotXS46 = [];
    var dotXS48 = [];

    var dotXS55 = [];
    var dotXS53 = [];
    var dotXS57 = [];
    var dotXS52 = [];
    var dotXS54 = [];
    var dotXS56 = [];
    var dotXS58 = [];

    var dotXS65 = [];
    var dotXS63 = [];
    var dotXS67 = [];
    var dotXS62 = [];
    var dotXS64 = [];
    var dotXS66 = [];
    var dotXS68 = [];

    var dotXS75 = [];
    var dotXS73 = [];
    var dotXS77 = [];
    var dotXS72 = [];
    var dotXS74 = [];
    var dotXS76 = [];
    var dotXS78 = [];

    /* ------------------------------------------------------------------------- */

    var dotLL0_x;
    var dotLL20_x;
    var dotLL40_x;
    var dotLL60_x;

    var dotCenter_x;

    var dotLL10_x;
    var dotLL30_x;
    var dotLL50_x;
    var dotLL70_x;

    var dotMM41_x;
    var dotMM42_x;
    var dotMM61_x;
    var dotMM62_x;

    var dotSS51_x;
    var dotSS52_x;
    var dotSS53_x;

    // Функция для чтения данных из таблицы PERSONAL/COMPATIBILITY
    function readTableData(suffix = "0") {
      const data = {
        paterna: [
          document.getElementById("pat1_" + suffix).textContent,
          document.getElementById("pat2_" + suffix).textContent,
          document.getElementById("pat3_" + suffix).textContent
        ],
        materna: [
          document.getElementById("mat1_" + suffix).textContent,
          document.getElementById("mat2_" + suffix).textContent,
          document.getElementById("mat3_" + suffix).textContent
        ],
        chakras: {
          sahasrara: [
            document.getElementById("cell_a1_" + suffix).textContent,
            document.getElementById("cell_a2_" + suffix).textContent,
            document.getElementById("cell_a3_" + suffix).textContent
          ],
          ajna: [
            document.getElementById("cell_b1_" + suffix).textContent,
            document.getElementById("cell_b2_" + suffix).textContent,
            document.getElementById("cell_b3_" + suffix).textContent
          ],
          vishuddha: [
            document.getElementById("cell_c1_" + suffix).textContent,
            document.getElementById("cell_c2_" + suffix).textContent,
            document.getElementById("cell_c3_" + suffix).textContent
          ],
          anahata: [
            document.getElementById("cell_d1_" + suffix).textContent,
            document.getElementById("cell_d2_" + suffix).textContent,
            document.getElementById("cell_d3_" + suffix).textContent
          ],
          manipura: [
            document.getElementById("cell_e1_" + suffix).textContent,
            document.getElementById("cell_e2_" + suffix).textContent,
            document.getElementById("cell_e3_" + suffix).textContent
          ],
          svadhisthana: [
            document.getElementById("cell_f1_" + suffix).textContent,
            document.getElementById("cell_f2_" + suffix).textContent,
            document.getElementById("cell_f3_" + suffix).textContent
          ],
          muladhara: [
            document.getElementById("cell_g1_" + suffix).textContent,
            document.getElementById("cell_g2_" + suffix).textContent,
            document.getElementById("cell_g3_" + suffix).textContent
          ],
          total: [
            document.getElementById("cell_h1_" + suffix).textContent,
            document.getElementById("cell_h2_" + suffix).textContent,
            document.getElementById("cell_h3_" + suffix).textContent
          ]
        }
      };
      console.log("Считанные данные из таблицы (suffix=" + suffix + "):", data);
      if (!data.chakras || !data.chakras.muladhara) {
        console.error("data.chakras или muladhara не определены!", data);
        return [];
      }
      return data;
    }

    // Функция маски ввода даты (формат dd.mm.yyyy)
    function dateEventMask(e) {
      if (!e.data) return;
      var val = e.data;
      var str = e.target.value;
      var len = str.length;
      if (typeof val === 'string' && !val.match(/[0-9.]/)) {
        e.target.value = str.substring(0, str.length - 1);
        return;
      }
      if (len === 2) { e.target.value += '.'; }
      if (len === 5) { e.target.value += '.'; }
    }

    // Функция для обработки нажатия Enter
    function handleEnter(event, callback) {
      if (event.key === "Enter") { callback(); }
    }

    function getPaidPoints() {
      let data = readTableData("0");
      console.log("data.chakras:", data.chakras);
      function safeParse(val) {
        const num = parseInt(val);
        return isNaN(num) ? 0 : num; // если не число — вернуть 0
      }
      const lineaPaternaValue = parseInt(data.paterna[0]);
      const lineaMaternaValue = parseInt(data.materna[0]);
      return [
        { name: "Energía masculina", value: lineaPaternaValue },
        { name: "Energía femenina", value: lineaMaternaValue },
        { name: "Cola kármica general", chakra: "Muladhara", aspect: "Fisica", value: safeParse(data.chakras.muladhara[0]) },
        { name: "Cola kármica del amor", chakra: "Svadhisthana", aspect: "Emociones", value: safeParse(data.chakras.svadhisthana[2]) },
        { name: "Pareja kármica en el amor", chakra: "Muladhara", aspect: "Emociones", value: safeParse(data.chakras.anahata[2]) },
        { name: "Amor y dinero", chakra: "Manipura", aspect: "Emociones", value: safeParse(data.chakras.anahata[2]) },
        { name: "Dirección de vida profesional", chakra: "Manipura", aspect: "Física", value: safeParse(data.chakras.vishuddha[0]) },
        { name: "Fuente de ingresos", chakra: "Manipura", aspect: "Energía", value: safeParse(data.chakras.manipura[1]) },
        { name: "Bloqueo financiero", chakra: "Muladhara", aspect: "Energia", value: safeParse(data.chakras.svadhisthana[1]) },
        
      ];
    }

    function savePaidPoints(orderId, points) {
      console.log("Попытка отправить points:", orderId, points);
      fetch('/api/payments/save-points', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          order_id: orderId,
          points: points
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          console.log("Points успешно сохранены на сервере!");
        } else {
          console.error("Ошибка при сохранении points:", data);
        }
      })
      .catch(error => {
        console.error("Ошибка при отправке points:", error);
      });
    }

    function calc_1() {
      console.log("Функция calc_1 сработала!");
    
      // Получаем дату из input
      var date1 = document.getElementById("inputDate1").value.trim();
      console.log("Дата из inputDate1:", date1);
    
      // Проверяем, введена ли дата
      if (!date1) {
        alert("Introduce tu fecha de nacimiento!");
        return;
      }
    
      // Обновляем таблицу (PERSONAL)
      calculate();
    
      // Показываем панель Matriz 1
      $('#panel1').show();
    
      // Первое сообщение в чат
      openChatWindow("¡Ya he analizado tu Matriz del Destino y estoy listo para compartir los primeros resultados! ☺️");
    
      // После вызова calculate() получаем реальные значения для бесплатных точек
      let data = readTableData("0");
      console.log("data:", data);
      if (!data || !data.chakras) {
        alert("Error: los datos no están listos. Inténtalo de nuevo.!");
        return;
      }
      let freePoints = [
        { name: "Zona de confort", chakra: "Anahata", aspect: "Fisica", value: parseInt(data.chakras.anahata[0]) },
        { name: "Recurso interior", chakra: "Sahasrara", aspect: "Fisica", value: parseInt(data.chakras.sahasrara[2]) },
        { name: "Talento", chakra: "Sahasrara", aspect: "Energia", value: parseInt(data.chakras.sahasrara[1]) }
      ];
    
      console.log("Собранные данные для бесплатной части:", freePoints);
    
      // Отправляем данные на сервер для бесплатной интерпретации
      fetch("/api/consult_personal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ free_points: freePoints })
      })
        .then(response => response.json())
        .then(data => {
          console.log("Ответ сервера:", data);
          if (data.message) {
            addBotMessage(data.message);
    
            // Через 2 секунды предлагаем платный расчёт
            setTimeout(function () {
              openChatWindow("✨ ¿Quieres acceder al análisis completo de tu matriz? (premium)?");
    
              // Создаём кнопки "Да" и "Нет"
              const chatArea = document.querySelector(".chat-area");
              const buttonContainer = document.createElement("div");
              buttonContainer.style.margin = "10px 0";
              buttonContainer.style.display = "flex";
              buttonContainer.style.gap = "10px";
    
              const yesBtn = document.createElement("button");
              yesBtn.textContent = "Sí";
              yesBtn.style.padding = "8px 16px";
              yesBtn.style.borderRadius = "20px";
              yesBtn.style.border = "2px solid #fff";
              yesBtn.style.backgroundColor = "#000";
              yesBtn.style.color = "#fff";
              yesBtn.style.cursor = "pointer";
    
              const noBtn = document.createElement("button");
              noBtn.textContent = "No";
              noBtn.style.padding = "8px 16px";
              noBtn.style.borderRadius = "20px";
              noBtn.style.border = "2px solid #fff";
              noBtn.style.backgroundColor = "#000";
              noBtn.style.color = "#fff";
              noBtn.style.cursor = "pointer";
    
              // Обработчик для кнопки "Да"
              yesBtn.addEventListener("click", async function () {
                chatArea.removeChild(buttonContainer);
                openChatWindow("¡Excelente! Ahora serás redirigido a la página de pago... Ingresa también tu número de teléfono!");

                // Создаём форму для ввода email и телефона
                  const inputDiv = document.createElement("div");
                  inputDiv.style.display = "flex";
                  inputDiv.style.flexDirection = "column";
                  inputDiv.style.gap = "8px";
                  inputDiv.style.margin = "10px 0";

                  const emailInput = document.createElement("input");
                  emailInput.type = "email";
                  emailInput.placeholder = "Introduce tu email";
                  emailInput.style.padding = "8px";
                  emailInput.style.borderRadius = "8px";
                  emailInput.style.border = "1px solid #ccc";

                  const phoneInput = document.createElement("input");
                  phoneInput.type = "tel";
                  phoneInput.placeholder = "Introduce tu teléfono";
                  phoneInput.style.padding = "8px";
                  phoneInput.style.borderRadius = "8px";
                  phoneInput.style.border = "1px solid #ccc";

                  const continueBtn = document.createElement("button");
                  continueBtn.textContent = "Continuar";
                  continueBtn.style.padding = "8px 16px";
                  continueBtn.style.borderRadius = "20px";
                  continueBtn.style.border = "2px solid #fff";
                  continueBtn.style.backgroundColor = "#000";
                  continueBtn.style.color = "#fff";
                  continueBtn.style.cursor = "pointer";

                  inputDiv.appendChild(emailInput);
                  inputDiv.appendChild(phoneInput);
                  inputDiv.appendChild(continueBtn);
                  chatArea.appendChild(inputDiv);
                  chatArea.scrollTop = chatArea.scrollHeight;

                  continueBtn.addEventListener("click", async function () {
                    const emailVal = emailInput.value.trim();
                    const phoneVal = phoneInput.value.trim();
                  if (!phoneVal) {
                    addBotMessage("Por favor, indique su teléfono!");
                      return;
                    }
                  const paidPoints = getPaidPoints();
                    const response = await fetch('/api/payments/create-link', {
                      method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      email: emailVal,
                      phone: phoneVal,
                      birth_date: date1,
                      type: "personal",
                      points: paidPoints
                    })
                    });
                    const data = await response.json();
                    const orderId = data.order_id;
                  if (!orderId) {
                    addBotMessage("Error: no se pudo obtener el número de pedido. Inténtelo más tarde.");
                    return;
                  }
                  localStorage.setItem("orderId", orderId);
                  localStorage.setItem("orderType", "personal");

                  if (data.payment_url) {
                    window.location.href = data.payment_url;
                  } else {
                    const amount = 2383;
                    const productName = "Персональный анализ";
                    let payUrl = `https://relacionesarmoniosas.payform.ru/?products[0][price]=${amount}&products[0][quantity]=1&products[0][name]=${encodeURIComponent(productName)}&order_id=${orderId}&do=pay`;
                    if (emailVal) payUrl += `&customer_email=${encodeURIComponent(emailVal)}`;
                    if (phoneVal) payUrl += `&customer_phone=${encodeURIComponent(phoneVal)}`;
                    window.location.href = payUrl;
                  }
                  });

                // Обработка Enter
                  emailInput.addEventListener("keydown", function(e) {
                    if (e.key === "Enter") continueBtn.click();
                  });
                  phoneInput.addEventListener("keydown", function(e) {
                    if (e.key === "Enter") continueBtn.click();
                });
              });
    
              // Обработчик для кнопки "Нет"
              noBtn.addEventListener("click", function () {
                chatArea.removeChild(buttonContainer);
                openChatWindow("¡Bien, continuamos sin la parte de pago!");
              });
    
              // Добавляем кнопки в чат
              buttonContainer.appendChild(yesBtn);
              buttonContainer.appendChild(noBtn);
              chatArea.appendChild(buttonContainer);
              chatArea.scrollTop = chatArea.scrollHeight;
            }, 2000);
          } else {
            console.error("Поле 'message' отсутствует в ответе сервера.");
            addBotMessage("Lo sentimos, se ha producido un error en el procesamiento de los datos.");
          }
        })
        .catch(error => {
          console.error("Ошибка при получении ответа:", error);
          addBotMessage("Lo sentimos, se ha producido un error.");
        });

      let paidPoints = getPaidPoints();
      localStorage.setItem("paidPoints", JSON.stringify(paidPoints));
    }
    
    
	  
  

    // Функция calc_2: для COMPATIBILITY
    function calc_2() {
      console.log("Функция calc_2 сработала!");
      var date1 = document.getElementById("inputDate1").value.trim();
      var date2 = document.getElementById("inputDate2").value.trim();
      console.log("Дата из inputDate1:", date1, "Дата из inputDate2:", date2);
      if (!date1 || !date2) {
        alert("Introduce ambas fechas!");
        return;
      }

      calculate(); // Обновляет таблицы (PERSONAL и COMPATIBILITY)
      $('#panelX').show();
      $('#panel2').show(); // Показываем панели для совместимости

      var personalData = readTableData("0");
      var compatibilityData = readTableData("1");

      var computed_personal = "Línea del padre: " + personalData.paterna.join(", ") +
                              " | Línea de la madre: " + personalData.materna.join(", ") +
                              " | Chakras: " +
                              "Sahasrara(" + personalData.chakras.sahasrara.join("/") + "), " +
                              "Ajna(" + personalData.chakras.ajna.join("/") + "), " +
                              "Vishuddha(" + personalData.chakras.vishuddha.join("/") + "), " +
                              "Anahata(" + personalData.chakras.anahata.join("/") + "), " +
                              "Manipura(" + personalData.chakras.manipura.join("/") + "), " +
                              "Svadhisthana(" + personalData.chakras.svadhisthana.join("/") + "), " +
                              "Muladhara(" + personalData.chakras.muladhara.join("/") + "), " +
                              "Total(" + personalData.chakras.total.join("/") + ")" +
                              " | Fecha: " + date1;

      var computed_compatibility = "Línea del padre: " + compatibilityData.paterna.join(", ") +
                                   " | Línea de la madre: " + compatibilityData.materna.join(", ") +
                                   " | Chakras: " +
                                   "Sahasrara(" + compatibilityData.chakras.sahasrara.join("/") + "), " +
                                   "Ajna(" + compatibilityData.chakras.ajna.join("/") + "), " +
                                   "Vishuddha(" + compatibilityData.chakras.vishuddha.join("/") + "), " +
                                   "Anahata(" + compatibilityData.chakras.anahata.join("/") + "), " +
                                   "Manipura(" + compatibilityData.chakras.manipura.join("/") + "), " +
                                   "Svadhisthana(" + compatibilityData.chakras.svadhisthana.join("/") + "), " +
                                   "Muladhara(" + compatibilityData.chakras.muladhara.join("/") + "), " +
                                   "Total(" + compatibilityData.chakras.total.join("/") + ")" +
                                   " | Fecha: " + date2;

      console.log("Отправляем данные для PERSONAL:", computed_personal);
      console.log("Отправляем данные для COMPATIBILITY:", computed_compatibility);

      // ... перед отправкой:
      var partner1 = readTableData("0"); // данные по первой дате
      var partner2 = readTableData("1"); // данные по второй дате

      fetch("/api/consult_compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          partner1: { chakras: partner1.chakras },
          partner2: { chakras: partner2.chakras }
        })
      })
      .then(response => response.json())
      .then(data => {
        openChatWindow(data.message);

        // Всегда показываем предложение об оплате совместимости
        // (не завися от точного текста ответа сервера)
          const chatArea = document.querySelector(".chat-area");
          const buttonContainer = document.createElement("div");
          buttonContainer.style.margin = "10px 0";
          buttonContainer.style.display = "flex";
          buttonContainer.style.gap = "10px";

          const yesBtn = document.createElement("button");
          yesBtn.textContent = "Sí";
          yesBtn.style.padding = "8px 16px";
          yesBtn.style.borderRadius = "20px";
          yesBtn.style.border = "2px solid #fff";
          yesBtn.style.backgroundColor = "#000";
          yesBtn.style.color = "#fff";
          yesBtn.style.cursor = "pointer";

          const noBtn = document.createElement("button");
          noBtn.textContent = "No";
          noBtn.style.padding = "8px 16px";
          noBtn.style.borderRadius = "20px";
          noBtn.style.border = "2px solid #fff";
          noBtn.style.backgroundColor = "#000";
          noBtn.style.color = "#fff";
          noBtn.style.cursor = "pointer";

          yesBtn.addEventListener("click", async function () {
            chatArea.removeChild(buttonContainer);
            openChatWindow("¡Perfecto! Ahora serás redirigido a la página de pago... ¡Introduce tu número de teléfono!");

            // Создаём форму для ввода email и телефона
              const inputDiv = document.createElement("div");
              inputDiv.style.display = "flex";
              inputDiv.style.flexDirection = "column";
              inputDiv.style.gap = "8px";
              inputDiv.style.margin = "10px 0";

              const emailInput = document.createElement("input");
              emailInput.type = "email";
              emailInput.placeholder = "Introduce tu email";
              emailInput.style.padding = "8px";
              emailInput.style.borderRadius = "8px";
              emailInput.style.border = "1px solid #ccc";

              const phoneInput = document.createElement("input");
              phoneInput.type = "tel";
              phoneInput.placeholder = "Introduce tu teléfono";
              phoneInput.style.padding = "8px";
              phoneInput.style.borderRadius = "8px";
              phoneInput.style.border = "1px solid #ccc";

              const continueBtn = document.createElement("button");
              continueBtn.textContent = "Continuar";
              continueBtn.style.padding = "8px 16px";
              continueBtn.style.borderRadius = "20px";
              continueBtn.style.border = "2px solid #fff";
              continueBtn.style.backgroundColor = "#000";
              continueBtn.style.color = "#fff";
              continueBtn.style.cursor = "pointer";

              inputDiv.appendChild(emailInput);
              inputDiv.appendChild(phoneInput);
              inputDiv.appendChild(continueBtn);
              chatArea.appendChild(inputDiv);
              chatArea.scrollTop = chatArea.scrollHeight;

              continueBtn.addEventListener("click", async function () {
                const emailVal = emailInput.value.trim();
                const phoneVal = phoneInput.value.trim();
              if (!phoneVal) {
                addBotMessage("¡Por favor, indique su teléfono!");
                  return;
                }
              var partner1 = readTableData("0");
              var partner2 = readTableData("1");
                const response = await fetch('/api/payments/create-link', {
                  method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  email: emailVal,
                  phone: phoneVal,
                  birth_date: `${date1}|${date2}`,
                  type: "compatibility",
                  points: [
                    partner1,
                    partner2
                  ]
                })
                });
                const data = await response.json();
                const orderId = data.order_id;
              if (!orderId) {
                addBotMessage("Error: no se pudo obtener el número de pedido. Inténtelo de nuevo más tarde.");
                return;
              }
              localStorage.setItem("orderId", orderId);
              localStorage.setItem("orderType", "compatibility");

              if (data.payment_url) {
                window.location.href = data.payment_url;
              } else {
                const amount = 2669;
                const productName = "Совместимость";
                let payUrl = `https://relacionesarmoniosas.payform.ru/?products[0][price]=${amount}&products[0][quantity]=1&products[0][name]=${encodeURIComponent(productName)}&order_id=${orderId}&do=pay`;
                if (emailVal) payUrl += `&customer_email=${encodeURIComponent(emailVal)}`;
                if (phoneVal) payUrl += `&customer_phone=${encodeURIComponent(phoneVal)}`;
                window.location.href = payUrl;
              }
              });

            // Обработка Enter
              emailInput.addEventListener("keydown", function(e) {
                if (e.key === "Enter") continueBtn.click();
              });
              phoneInput.addEventListener("keydown", function(e) {
                if (e.key === "Enter") continueBtn.click();
            });
          });

          noBtn.addEventListener("click", function () {
            chatArea.removeChild(buttonContainer);
            openChatWindow("¡De acuerdo, continuamos sin la parte de pago!");
          });

          buttonContainer.appendChild(yesBtn);
          buttonContainer.appendChild(noBtn);
          chatArea.appendChild(buttonContainer);
          chatArea.scrollTop = chatArea.scrollHeight;
      })
      .catch(error => {
        console.error("Ошибка при получении ответа:", error);
        addBotMessage("Lo sentimos, ha ocurrido un error.");
      });
    }

    // Логика чата и прочие функции
    let idleTimer;
    let autoOpenEnabled = true;
    const positives = ["да", "да!", "yes", "si", "sí", "ok", "готов"];
    const negatives = ["нет", "no", "не хочу", "не готов", "не"];

    function resetIdleTimer() {
		clearTimeout(idleTimer);
		if (autoOpenEnabled) {
		  // Здесь ставится таймер на 3 секунд (3000 мс)
		  idleTimer = setTimeout(() => { openChatWindow(); }, 3000);
		}
	  }

    // Скрыть вступительные подзаголовки в окне чата на мобильных,
    // когда появляется первое содержательное сообщение бота
    function collapseIntroForMobile() {
      try {
        const isDesktop = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) >= 992;
        if (isDesktop) return; // только не-десктоп
        const chatWindow = document.getElementById("chatWindow");
        if (chatWindow && !chatWindow.classList.contains("intro-collapsed")) {
          chatWindow.classList.add("intro-collapsed");
        }
      } catch (e) {
        console.warn('collapseIntroForMobile failed', e);
      }
    }

    function openChatWindow(botMessage) {
      const chatWindow = document.getElementById("chatWindow");
      chatWindow.style.display = "block";
      const chatArea = document.querySelector(".chat-area");
      // Проверяем, был ли пользователь внизу чата
      const isAtBottom = chatArea.scrollHeight - chatArea.scrollTop - chatArea.clientHeight < 10;
      if (botMessage) {
        const botMessageDiv = document.createElement("div");
        botMessageDiv.classList.add("message", "bot-message");
        botMessageDiv.textContent = "CHATBOT AI: " + botMessage;
        chatArea.appendChild(botMessageDiv);
        // как только появилось первое содержательное сообщение — скрываем intro (мобильные)
        collapseIntroForMobile();
      }
      if (isAtBottom) {
      chatArea.scrollTop = chatArea.scrollHeight;
      }
    }

    function addBotMessage(text) {
      const chatArea = document.querySelector(".chat-area");
      const isAtBottom = chatArea.scrollHeight - chatArea.scrollTop - chatArea.clientHeight < 10;
      const botMsg = document.createElement("div");
      botMsg.classList.add("message", "bot-message");
      botMsg.textContent = "CHATBOT AI: " + text;
      chatArea.appendChild(botMsg);
      // любое сообщение бота — сворачиваем intro на мобильных
      collapseIntroForMobile();
      if (isAtBottom) {
        chatArea.scrollTop = chatArea.scrollHeight;
      }
    }

    // Минимальная реализация отправки сообщения из поля ввода
    function sendMessage() {
      const input = document.querySelector('.input-area input');
      const msg = (input.value || '').trim();
      if (!msg) return;
      const chatArea = document.querySelector('.chat-area');
      const isAtBottom = chatArea.scrollHeight - chatArea.scrollTop - chatArea.clientHeight < 10;

      // Добавляем сообщение пользователя
      const userMsg = document.createElement('div');
      userMsg.classList.add('message', 'user-message');
      userMsg.textContent = msg;
      chatArea.appendChild(userMsg);
      input.value = '';
      if (isAtBottom) chatArea.scrollTop = chatArea.scrollHeight;

      // Отправляем на бэкенд и показываем ответ
      fetch('/api/get_answer_async', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: msg })
      })
      .then(r => r.json())
      .then(data => {
        if (data && data.message) {
          addBotMessage(data.message);
        } else {
          addBotMessage('No tengo una respuesta en este momento.');
        }
      })
      .catch(err => {
        console.error('sendMessage error:', err);
        addBotMessage('Lo sentimos, se ha producido un error.');
      })
      .finally(() => {
        resetIdleTimer();
      });
    }

    // Карточка со ссылкой на PDF после оплаты
    function addPdfLink(orderId, type) {
      const chatArea = document.querySelector('.chat-area');
      const isAtBottom = chatArea.scrollHeight - chatArea.scrollTop - chatArea.clientHeight < 10;

      const card = document.createElement('div');
      // Убираем зелёную рамку
      card.style.border = 'none';
      card.style.borderRadius = '12px';
      card.style.padding = '14px';
      card.style.margin = '12px 0';
      // Убираем зелёный фон
      card.style.background = 'transparent';
      card.style.color = '#eaffea';

      const title = document.createElement('div');
      title.style.display = 'flex';
      title.style.alignItems = 'center';
      title.style.gap = '8px';
      const check = document.createElement('span');
      check.textContent = '✔';
      check.style.color = '#2ecc71';
      const h = document.createElement('strong');
      h.textContent = 'Archivo listo para descargar';
      title.appendChild(check);
      title.appendChild(h);

      const sub = document.createElement('div');
      sub.style.marginTop = '4px';
      sub.textContent = 'El informe está preparado. ¡Puedes abrirlo ahora!';

      const name = document.createElement('div');
      name.style.marginTop = '8px';
      name.style.fontStyle = 'italic';
      // Добавляем иконку документа перед названием
      name.textContent = (type === 'compatibility' ? '📄 Informe de compatibilidad.pdf' : '📄 Informe personal.pdf');

      const btn = document.createElement('a');
      // Кнопка: иконка стрелки в белом кружке слева + текст
      const iconWrap = document.createElement('span');
      iconWrap.textContent = '⬇';
      iconWrap.style.display = 'inline-flex';
      iconWrap.style.alignItems = 'center';
      iconWrap.style.justifyContent = 'center';
      iconWrap.style.width = '22px';
      iconWrap.style.height = '22px';
      iconWrap.style.borderRadius = '50%';
      // Белая стрелка на тёмном фоне для читаемости
      iconWrap.style.background = '#111';
      iconWrap.style.color = '#fff';
      iconWrap.style.marginRight = '8px';

      const btnText = document.createElement('span');
      btnText.textContent = 'Descargar archivo';
      const pdfUrl = type === 'compatibility'
        ? `/api/payments/compatibility-interpretation-pdf?order_id=${encodeURIComponent(orderId)}`
        : `/api/payments/paid-interpretation-pdf?order_id=${encodeURIComponent(orderId)}`;
      btn.href = pdfUrl;
      btn.target = '_blank';
      btn.rel = 'noopener noreferrer';
      btn.style.display = 'inline-flex';
      btn.style.alignItems = 'center';
      btn.style.marginTop = '10px';
      btn.style.padding = '10px 16px';
      // Белый фон кнопки
      btn.style.background = '#ffffff';
      btn.style.borderRadius = '20px';
      btn.style.color = '#111';
      btn.style.fontWeight = '600';
      btn.style.textDecoration = 'none';

      card.appendChild(title);
      card.appendChild(sub);
      card.appendChild(name);
      btn.appendChild(iconWrap);
      btn.appendChild(btnText);
      card.appendChild(btn);

      const wrapper = document.createElement('div');
      wrapper.classList.add('message', 'bot-message');
      wrapper.appendChild(card);

      chatArea.appendChild(wrapper);
      if (isAtBottom) chatArea.scrollTop = chatArea.scrollHeight;
    }
  // ================================================
  // Инициализация при загрузке страницы
  // ================================================
  document.addEventListener("DOMContentLoaded", function() {
    calculate();

    const params = new URLSearchParams(window.location.search);
    let orderId = params.get('order_id');
    if (!orderId || orderId.startsWith('{')) {
      orderId = params.get('_payform_order_id');
    }
    if (!orderId) {
      orderId = localStorage.getItem("orderId");
    }
    console.log("orderId:", orderId);

    // Показываем ошибку только если в URL есть параметры оплаты, но orderId не определён
    if (orderId) {
        document.getElementById("chatWindow").style.display = "block";
        openChatWindow("¡Gracias por el pago! Tu resultado se mostrará a continuación.");
    } else if (
        window.location.search.includes("order_id") ||
        window.location.search.includes("_payform_order_id")
    ) {
        addBotMessage("Error: no se pudo determinar el número de pedido. Por favor, inténtalo de nuevo o contacta con el soporte.");
    }
    // Если пользователь просто зашёл на сайт — ничего не показываем, чат-бот работает как обычно

    // Получаем points из localStorage
    let points = [];
    try {
      points = JSON.parse(localStorage.getItem("paidPoints") || "[]");
    } catch (e) {
      points = [];
    }

    // --- ВОТ ЗДЕСЬ ВСТАВЬ ПРОВЕРКУ ---
    // Можно попробовать определить тип заказа по points или по localStorage (например, если points.length === 2 и есть chakras — это совместимость)
    let isCompatibility = false;
    if (points.length === 2 && points[0].chakras && points[1].chakras) {
      isCompatibility = true;
    }

    if (orderId && points.length && points.some(p => p.value > 0)) {
      savePaidPoints(orderId, points);
      if (isCompatibility) {
        pollCompatibilityResult(orderId, 120, 3000);
      } else {
        pollPaidInterpretation(orderId, 120, 3000);
      }
      localStorage.removeItem("paidPoints");
    } else if (orderId) {
      // Новый надёжный способ определения типа заказа
      async function ensureOrderType(orderId) {
        let orderType = localStorage.getItem("orderType");
        if (orderType) return orderType;

        // Если нет в localStorage — узнаём у сервера
        try {
          const resp = await fetch(`/api/payments/order-type?order_id=${orderId}`);
          const data = await resp.json();
          if (data.type) {
            localStorage.setItem("orderType", data.type);
            return data.type;
          }
        } catch (e) {
          console.error("Не удалось получить тип заказа с сервера:", e);
        }
        return null;
      }

      (async function() {
        let orderType = await ensureOrderType(orderId);

        if (orderType === "compatibility") {
          pollCompatibilityResult(orderId, 120, 3000);
        } else if (orderType === "personal") {
          pollPaidInterpretation(orderId, 120, 3000);
        } else {
          addBotMessage("No se pudo determinar el tipo de pedido. Por favor, inténtalo de nuevo o contacta con el soporte.");
        }
      })();
    }

    // Применяем маску ввода для полей дат
    document.getElementById("inputDate1").addEventListener("input", dateEventMask);
    document.getElementById("inputDate2").addEventListener("input", dateEventMask);

    // Настройка плавающей кнопки чата
    document.getElementById("floatingBtn").addEventListener("click", function() {
      autoOpenEnabled = true;
      document.getElementById("chatWindow").style.display = "block";
      resetIdleTimer();
    });

    // Управление окном чата
    document.querySelector(".chat-controls .chat-close").addEventListener("click", function() {
      autoOpenEnabled = false;
      clearTimeout(idleTimer);
      document.querySelector(".chat-area").innerHTML = "";
      document.getElementById("chatWindow").style.display = "none";
    });

    document.querySelector(".chat-controls .chat-minimize").addEventListener("click", function() {
      autoOpenEnabled = true;
      document.getElementById("chatWindow").style.display = "none";
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => { openChatWindow(); }, 30000);
    });

    document.getElementById("startNewChat").addEventListener("click", function() {
      document.querySelector(".chat-area").innerHTML = "";
      resetIdleTimer();
    });

    document.getElementById("sendBtn").addEventListener("click", sendMessage);
    document.querySelector(".input-area input").addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        sendMessage();
        e.preventDefault();
      }
    });

    ['mousemove', 'keydown', 'scroll', 'click'].forEach(function(evt) {
      window.addEventListener(evt, resetIdleTimer);
    });
    resetIdleTimer();
  });



  /* ------------------------------------------------------------------------- */
  /* --------- CALCULATE ----------------------------------------------------- */
  /* ------------------------------------------------------------------------- */

  function calc(i, dateVal)
  {
    console.log(i);
    console.log(dateVal);
    
    var dd = dateVal.split('.')[0];
    var mm = dateVal.split('.')[1];
    var yyyy = dateVal.split('.')[2];

    dotLL0[i] = parseInt(sum22(dd));
    dotLL20[i] = parseInt(sum22(mm));
    dotLL40[i] = parseInt(sum22(yyyy.toString()));
    dotLL60[i] = parseInt(sum22(dd + mm + yyyy));

    dotCenter[i] = base22(dotLL0[i] + dotLL20[i] + dotLL40[i] + dotLL60[i]);

    dotLL10[i] = base22(dotLL0[i] + dotLL20[i]);
    dotLL30[i] = base22(dotLL20[i] + dotLL40[i]);
    dotLL50[i] = base22(dotLL40[i] + dotLL60[i]);
    dotLL70[i] = base22(dotLL0[i] + dotLL60[i]);

    dotMM02[i] = base22(dotCenter[i] + dotLL0[i]); 
    dotMM01[i] = base22(dotMM02[i] + dotLL0[i]);
    dotMM22[i] = base22(dotCenter[i] + dotLL20[i]);
    dotMM21[i] = base22(dotMM22[i] + dotLL20[i]);
    dotMM42[i] = base22(dotCenter[i] + dotLL40[i]);
    dotMM41[i] = base22(dotMM42[i] + dotLL40[i]);
    dotMM62[i] = base22(dotCenter[i] + dotLL60[i]);
    dotMM61[i] = base22(dotMM62[i] + dotLL60[i]);

    dotSS11[i] = base22(dotLL0[i] + dotLL20[i]);
    dotSS12[i] = base22(dotMM01[i] + dotMM21[i]);
    dotSS13[i] = base22(dotMM02[i] + dotMM22[i]);
    dotSS51[i] = base22(dotLL40[i] + dotLL60[i]);
    dotSS52[i] = base22(dotMM41[i] + dotMM61[i]);
    dotSS53[i] = base22(dotMM42[i] + dotMM62[i]);

    dotMMC1[i] = base22(dotLL10[i] + dotLL30[i] + dotLL50[i] + dotLL70[i]);
    dotSSC1[i] = base22(dotCenter[i] + dotLL40[i]);

    dotXS5[i] = base22(dotLL0[i] + dotLL10[i]);
    dotXS3[i] = base22(dotLL0[i] + dotXS5[i]);
    dotXS7[i] = base22(dotXS5[i] + dotLL10[i]);
    dotXS2[i] = base22(dotLL0[i] + dotXS3[i]);
    dotXS4[i] = base22(dotXS3[i] + dotXS5[i]);
    dotXS6[i] = base22(dotXS5[i] + dotXS7[i]);
    dotXS8[i] = base22(dotXS7[i] + dotLL10[i]);
    
    dotXS15[i] = base22(dotLL10[i] + dotLL20[i]);
    dotXS13[i] = base22(dotLL10[i] + dotXS15[i]);
    dotXS17[i] = base22(dotXS15[i] + dotLL20[i]);
    dotXS12[i] = base22(dotLL10[i] + dotXS13[i]);
    dotXS14[i] = base22(dotXS13[i] + dotXS15[i]);
    dotXS16[i] = base22(dotXS15[i] + dotXS17[i]);
    dotXS18[i] = base22(dotXS17[i] + dotLL20[i]);

    dotXS25[i] = base22(dotLL20[i] + dotLL30[i]);
    dotXS23[i] = base22(dotLL20[i] + dotXS25[i]);
    dotXS27[i] = base22(dotXS25[i] + dotLL30[i]);
    dotXS22[i] = base22(dotLL20[i] + dotXS23[i]);
    dotXS24[i] = base22(dotXS23[i] + dotXS25[i]);
    dotXS26[i] = base22(dotXS25[i] + dotXS27[i]);
    dotXS28[i] = base22(dotXS27[i] + dotLL30[i]);

    dotXS35[i] = base22(dotLL30[i] + dotLL40[i]);
    dotXS33[i] = base22(dotLL30[i] + dotXS35[i]);
    dotXS37[i] = base22(dotXS35[i] + dotLL40[i]);
    dotXS32[i] = base22(dotLL30[i] + dotXS33[i]);
    dotXS34[i] = base22(dotXS33[i] + dotXS35[i]);
    dotXS36[i] = base22(dotXS35[i] + dotXS37[i]);
    dotXS38[i] = base22(dotXS37[i] + dotLL40[i]);

    dotXS45[i] = base22(dotLL40[i] + dotLL50[i]);
    dotXS43[i] = base22(dotLL40[i] + dotXS45[i]);
    dotXS47[i] = base22(dotXS45[i] + dotLL50[i]);
    dotXS42[i] = base22(dotLL40[i] + dotXS43[i]);
    dotXS44[i] = base22(dotXS43[i] + dotXS45[i]);
    dotXS46[i] = base22(dotXS45[i] + dotXS47[i]);
    dotXS48[i] = base22(dotXS47[i] + dotLL50[i]);

    dotXS55[i] = base22(dotLL50[i] + dotLL60[i]);
    dotXS53[i] = base22(dotLL50[i] + dotXS55[i]);
    dotXS57[i] = base22(dotXS55[i] + dotLL60[i]);
    dotXS52[i] = base22(dotLL50[i] + dotXS53[i]);
    dotXS54[i] = base22(dotXS53[i] + dotXS55[i]);
    dotXS56[i] = base22(dotXS55[i] + dotXS57[i]);
    dotXS58[i] = base22(dotXS57[i] + dotLL60[i]);

    dotXS65[i] = base22(dotLL60[i] + dotLL70[i]);
    dotXS63[i] = base22(dotLL60[i] + dotXS65[i]);
    dotXS67[i] = base22(dotXS65[i] + dotLL70[i]);
    dotXS62[i] = base22(dotLL60[i] + dotXS63[i]);
    dotXS64[i] = base22(dotXS63[i] + dotXS65[i]);
    dotXS66[i] = base22(dotXS65[i] + dotXS67[i]);
    dotXS68[i] = base22(dotXS67[i] + dotLL70[i]);

    dotXS75[i] = base22(dotLL70[i] + dotLL0[i]);
    dotXS73[i] = base22(dotLL70[i] + dotXS75[i]);
    dotXS77[i] = base22(dotXS75[i] + dotLL0[i]);
    dotXS72[i] = base22(dotLL70[i] + dotXS73[i]);
    dotXS74[i] = base22(dotXS73[i] + dotXS75[i]);
    dotXS76[i] = base22(dotXS75[i] + dotXS77[i]);
    dotXS78[i] = base22(dotXS77[i] + dotLL0[i]);
  }

  function calc_x()
  {
    dotLL0_x = base22(dotLL0[0] + dotLL0[1]);
    dotLL20_x = base22(dotLL20[0] + dotLL20[1]);
    dotLL40_x = base22(dotLL40[0] + dotLL40[1]);
    dotLL60_x = base22(dotLL60[0] + dotLL60[1]);

    dotCenter_x = base22(dotCenter[0] + dotCenter[1]);

    dotLL10_x = base22(dotLL10[0] + dotLL10[1]);
    dotLL30_x = base22(dotLL30[0] + dotLL30[1]);
    dotLL50_x = base22(dotLL50[0] + dotLL50[1]);
    dotLL70_x = base22(dotLL70[0] + dotLL70[1]);

    dotMM42_x = base22(dotLL40_x + dotCenter_x);
    dotMM41_x = base22(dotLL40_x + dotMM42_x);
    dotMM62_x = base22(dotLL60_x + dotCenter_x);
    dotMM61_x = base22(dotLL60_x + dotMM62_x);

    dotSS51_x = base22(dotLL40_x + dotLL60_x);
    dotSS52_x = base22(dotMM41_x + dotMM61_x);
    dotSS53_x = base22(dotMM42_x + dotMM62_x);
  }

  /* ------------------------------------------------------------------------- */
  /* --------- BASE 22 ------------------------------------------------------- */
  /* ------------------------------------------------------------------------- */

  _limitValue = function (value) 
  {
    var result = parseInt(value);
    while (result > 22) 
    {
      result = (result + "").split("").map((i) => (x += parseInt(i)), (x = 0)).reverse()[0];
    }
    return result;
  };

  function sum22(value) {
    value = Number(value);
    while (value > 22) {
      value = value.toString().split('').reduce((a, b) => a + Number(b), 0);
    }
    return value;
  }

  function base22(value)
  {
    if (value <= 22) 
    {
      return value;
    }
    else
    {
      return sum22(value.toString());
    }
  }

  /* ------------------------------------------------------------------------- */
  /* --------- POPULATE ------------------------------------------------------ */
  /* ------------------------------------------------------------------------- */

  function addSvgText_(x, y, value, fontSize, color)
  {
    var svgText = document.createElementNS(svgNS, "text");
    svgText.setAttributeNS(null,"font-family", "Verdana");
    svgText.setAttributeNS(null,"font-size", fontSize);
    svgText.setAttributeNS(null,"alignment-baseline", "middle");
    svgText.setAttributeNS(null,"text-anchor", "middle");
    svgText.setAttributeNS(null,"x", x);
    svgText.setAttributeNS(null,"y", y);
    svgText.setAttributeNS(null,"fill", color);
    svgText.innerHTML = value;
    svgLayer.appendChild(svgText); 
  }

  function addSvgText(x, y, value, fontSize)
  {
    addSvgText_(x, y, value, fontSize, "#fff");
  }

  function addAgeValue(x, y, value)
  {
    addSvgText_(x, y, value, "3", "#666");
  }

  function fillSvgX()
  {
    // --- main years old -----
    addSvgText(37, 127, dotLL0_x, 8);
    addSvgText(63.360390, 63.360390, dotLL10_x, 8);
    addSvgText(127, 37, dotLL20_x, 8);
    addSvgText(190.639610, 63.360390, dotLL30_x, 8);
    addSvgText(217, 127, dotLL40_x, 8);
    addSvgText(190.639610, 190.639610, dotLL50_x, 8);
    addSvgText(127, 217, dotLL60_x, 8);
    addSvgText(63.360390, 190.639610, dotLL70_x, 8);

    // --- center value -----
    addSvgText(127, 127, dotCenter_x, 8);

    // --- medium values -----
    addSvgText(200.5, 127, dotMM41_x, 5);
    addSvgText(187.5, 127, dotMM42_x, 5);
    addSvgText(127, 200.5, dotMM61_x, 5);
    addSvgText(127, 187.5, dotMM62_x, 5);

    // --- small values -----
    addSvgText(158.5, 158.5, dotSS53_x, 4);
    addSvgText(165, 165, dotSS52_x, 4);
    addSvgText(172, 172, dotSS51_x, 4);
  }

  function fillSvg(i)
  {
    // --- main years old -----
    addSvgText(37, 127, dotLL0[i], 8);
    addSvgText(63.360390, 63.360390, dotLL10[i], 8);
    addSvgText(127, 37, dotLL20[i], 8);
    addSvgText(190.639610, 63.360390, dotLL30[i], 8);
    addSvgText(217, 127, dotLL40[i], 8);
    addSvgText(190.639610, 190.639610, dotLL50[i], 8);
    addSvgText(127, 217, dotLL60[i], 8);
    addSvgText(63.360390, 190.639610, dotLL70[i], 8);

    // --- center value -----
    addSvgText(127, 127, dotCenter[i], 8);

    // --- medium values -----
    addSvgText(53.5, 127, dotMM01[i], 5);
    addSvgText(66.5, 127, dotMM02[i], 5);
    addSvgText(127, 53.5, dotMM21[i], 5);
    addSvgText(127, 66.5, dotMM22[i], 5);
    addSvgText(200.5, 127, dotMM41[i], 5);
    addSvgText(187.5, 127, dotMM42[i], 5);
    addSvgText(127, 200.5, dotMM61[i], 5);
    addSvgText(127, 187.5, dotMM62[i], 5);

    // --- small values -----
    addSvgText(82, 82, dotSS11[i], 4);
    addSvgText(89, 89, dotSS12[i], 4);
    addSvgText(95.5, 95.5, dotSS13[i], 4);
    addSvgText(158.5, 158.5, dotSS53[i], 4);
    addSvgText(165, 165, dotSS52[i], 4);
    addSvgText(172, 172, dotSS51[i], 4);

    // --- new values -----
    addSvgText(144, 127, dotMMC1[i], 5);
    addSvgText(155, 127, dotSSC1[i], 4);

    // --- years old -----
    addAgeValue(33.218854, 112.512988, dotXS2[i]);
    addAgeValue(34.735378, 104.888909, dotXS3[i]);
    addAgeValue(36.845405, 97.407318, dotXS4[i]);
    addAgeValue(39.535926, 90.114340, dotXS5[i]);
    addAgeValue(42.790354, 83.054941, dotXS6[i]);
    addAgeValue(46.588624, 76.272642, dotXS7[i]);
    addAgeValue(50.907318, 69.809260, dotXS8[i]);
    addAgeValue(70.809260, 50.907318, dotXS12[i]);
    addAgeValue(77.272642, 46.588624, dotXS13[i]);
    addAgeValue(84.054941, 42.790354, dotXS14[i]);
    addAgeValue(91.114340, 39.535926, dotXS15[i]);
    addAgeValue(98.407318, 36.845405, dotXS16[i]);
    addAgeValue(105.888909, 34.735378, dotXS17[i]);
    addAgeValue(113.512988, 33.218854, dotXS18[i]);
    addAgeValue(141.487012, 33.218854, dotXS22[i]);
    addAgeValue(149.111091, 34.735378, dotXS23[i]);
    addAgeValue(156.592682, 36.845405, dotXS24[i]);
    addAgeValue(163.885660, 39.535926, dotXS25[i]);
    addAgeValue(170.945059, 42.790354, dotXS26[i]);
    addAgeValue(177.727358, 46.588624, dotXS27[i]);
    addAgeValue(184.190740, 50.907318, dotXS28[i]);
    addAgeValue(203.092682, 69.809260, dotXS32[i]);
    addAgeValue(207.411376, 76.272642, dotXS33[i]);
    addAgeValue(211.209646, 83.054941, dotXS34[i]);
    addAgeValue(214.464074, 90.114340, dotXS35[i]);
    addAgeValue(217.154595, 97.407318, dotXS36[i]);
    addAgeValue(219.264622, 104.888909, dotXS37[i]);
    addAgeValue(220.781146, 112.512988, dotXS38[i]);
    addAgeValue(220.781146, 141.487012, dotXS42[i]);
    addAgeValue(219.264622, 149.111091, dotXS43[i]);
    addAgeValue(217.154595, 156.592682, dotXS44[i]);
    addAgeValue(214.464074, 163.885660, dotXS45[i]);
    addAgeValue(211.209646, 170.945059, dotXS46[i]);
    addAgeValue(207.411376, 177.727358, dotXS47[i]);
    addAgeValue(203.092682, 184.190740, dotXS48[i]);
    addAgeValue(184.190740, 203.092682, dotXS52[i]);
    addAgeValue(177.727358, 207.411376, dotXS53[i]);
    addAgeValue(170.945059, 211.209646, dotXS54[i]);
    addAgeValue(163.885660, 214.464074, dotXS55[i]);
    addAgeValue(156.592682, 217.154595, dotXS56[i]);
    addAgeValue(149.111091, 219.264622, dotXS57[i]);
    addAgeValue(141.487012, 220.781146, dotXS58[i]);
    addAgeValue(113.512988, 220.781146, dotXS62[i]);
    addAgeValue(105.888909, 219.264622, dotXS63[i]);
    addAgeValue(98.407318, 217.154595, dotXS64[i]);
    addAgeValue(91.114340, 214.464074, dotXS65[i]);
    addAgeValue(84.054941, 211.209646, dotXS66[i]);
    addAgeValue(77.272642, 207.411376, dotXS67[i]);
    addAgeValue(70.809260, 203.092682, dotXS68[i]);
    addAgeValue(50.907318, 184.190740, dotXS72[i]);
    addAgeValue(46.588624, 177.727358, dotXS73[i]);
    addAgeValue(42.790354, 170.945059, dotXS74[i]);
    addAgeValue(39.535926, 163.885660, dotXS75[i]);
    addAgeValue(36.845405, 156.592682, dotXS76[i]);
    addAgeValue(34.735378, 149.111091, dotXS77[i]);
    addAgeValue(33.218854, 141.487012, dotXS78[i]);
  }

  /* ------------------------------------------------------------------------- */

  function setCellValue22(id, value)
  {
    document.getElementById(id).innerHTML = base22(value);
  }

  function populateA(i)
  {
    setCellValue22("mat1_" + i, dotLL30[i]);
    setCellValue22("mat2_" + i, dotLL70[i]);
    setCellValue22("mat3_" + i, (dotLL30[i] + dotLL70[i]));
    setCellValue22("pat1_" + i, dotLL10[i]);
    setCellValue22("pat2_" + i, dotLL50[i]);
    setCellValue22("pat3_" + i, (dotLL10[i] + dotLL50[i]));
  }

  function populateB(i)
  {
    setCellValue22("cell_a1_" + i, dotLL0[i]);
    setCellValue22("cell_a2_" + i, dotLL20[i]);
    setCellValue22("cell_a3_" + i, dotSS11[i]);

    setCellValue22("cell_b1_" + i, dotMM01[i]);
    setCellValue22("cell_b2_" + i, dotMM21[i]);
    setCellValue22("cell_b3_" + i, dotSS12[i]);

    setCellValue22("cell_c1_" + i, dotMM02[i]);
    setCellValue22("cell_c2_" + i, dotMM22[i]);
    setCellValue22("cell_c3_" + i, dotSS13[i]);

    setCellValue22("cell_d1_" + i, dotCenter[i]);
    setCellValue22("cell_d2_" + i, dotCenter[i]);
    setCellValue22("cell_d3_" + i, base22(dotCenter[i] * 2));

    setCellValue22("cell_e1_" + i, dotMM42[i]);
    setCellValue22("cell_e2_" + i, dotMM62[i]);
    setCellValue22("cell_e3_" + i, dotSS53[i]);

    setCellValue22("cell_f1_" + i, dotMM41[i]);
    setCellValue22("cell_f2_" + i, dotMM61[i]);
    setCellValue22("cell_f3_" + i, dotSS52[i]);

    setCellValue22("cell_g1_" + i, dotLL40[i]);
    setCellValue22("cell_g2_" + i, dotLL60[i]);
    setCellValue22("cell_g3_" + i, dotSS51[i]);
    
    var total_h1 = dotLL0[i] + dotMM01[i] + dotMM02[i] + dotCenter[i] + dotMM42[i] + dotMM41[i] + dotLL40[i];
    setCellValue22("cell_h1_" + i, total_h1);
    var total_h2 = dotLL20[i] + dotMM21[i] + dotMM22[i] + dotCenter[i] + dotMM62[i] + dotMM61[i] + dotLL60[i];
    setCellValue22("cell_h2_" + i, total_h2);
    var total_h3 = base22(total_h1) + base22(total_h2);
    setCellValue22("cell_h3_" + i, total_h3);
  }

  /* ------------------------------------------------------------------------- */
  /* ------------------------------------------------------------------------- */
  /* ------------------------------------------------------------------------- */

  function setSvg_x()
  {
    svg = svg_x;

    if (typeof(svgLayer_x) != 'undefined' && svgLayer_x != null)
    {
      svgLayer_x.parentNode.removeChild(svgLayer_x);
    }
    svgLayer_x = document.createElementNS(svgNS, "g");
    svgLayer_x.setAttributeNS(null, "id", "svgGroupLayer_x");
    svg.appendChild(svgLayer_x);

    svgLayer = svgLayer_x;
  }

  function setSvg_0()
  {
    svg = svg_0;

    if (typeof(svgLayer_0) != 'undefined' && svgLayer_0 != null)
    {
      svgLayer_0.parentNode.removeChild(svgLayer_0);
    }
    svgLayer_0 = document.createElementNS(svgNS, "g");
    svgLayer_0.setAttributeNS(null, "id", "svgGroupLayer_0");
    svg.appendChild(svgLayer_0);

    svgLayer = svgLayer_0;
  }

  function setSvg_1()
  {
    svg = svg_1;

    if (typeof(svgLayer_1) != 'undefined' && svgLayer_1 != null)
    {
      svgLayer_1.parentNode.removeChild(svgLayer_1);
    }
    svgLayer_1 = document.createElementNS(svgNS, "g");
    svgLayer_1.setAttributeNS(null, "id", "svgGroupLayer_1");
    svg.appendChild(svgLayer_1);

    svgLayer = svgLayer_1;
  }

  // ---------------------------------------------------------------

  function getAge (element, date) 
  {
    var arr = date.split(".");
    var value = (new Date() - new Date(arr[2] + "-" + arr[1] + "-" + arr[0] + "T00:00")) / (1000 * 60 * 60 * 24 * 365);
    var message = "";
    if (value < 1) {
      message = "0 años";
    } else if (value > 1 && value < 2) {
      message = parseInt(value) + " año";
    } else {
      message = Math.floor(value) + " años";
    }
    element.innerHTML = message;
  };

  // ---------------------------------------------------------------

  function calculate()
  {
    // Сначала скрываем все панели
    $('#panel0').hide();
    $('#panelX').hide(); 
    $('#panel1').hide(); 
    $('#panel2').hide();

    // Считываем даты из полей ввода
    var dateVal_0 = document.getElementById('inputDate1').value;
    var dateVal_1 = document.getElementById('inputDate2').value;

    // 1) Проверяем первую дату
    if (dateVal_0.match(dateformat)) 
    {
      // Расчёты для первой матрицы
      var age_0 = document.getElementById('age_0');
      getAge(age_0, dateVal_0);   // Расчёт возраста (для заголовка)
      
      calc(0, dateVal_0);        // Заполнение массива dotLL..., dotMM..., dotSS... с индексом [0]
      setSvg_0();                // Готовим слой для отрисовки
      fillSvg(0);                // Рисуем "Матрицу 1"

      populateA(0);              // Заполняем таблицу (Линия отца/матери)
      populateB(0);              // Заполняем таблицу "карты здоровья"

      // Показываем панель с результатом "Матрица 1"
      $('#panel1').show();  

      // 2) Если введена и корректна ВТОРАЯ дата — делаем расчёт совместимости и "Матрицу 2"
      if (dateVal_1.match(dateformat)) 
      {
        var age_1 = document.getElementById('age_1');
        getAge(age_1, dateVal_1); // Возраст для второй даты

        calc(1, dateVal_1);      // Заполнение массивов dotLL..., dotMM..., dotSS... c индексом [1]
        calc_x();                // Расчёт для совместимости (X)

        // Рисуем "Матрицу 2"
        setSvg_1();
        fillSvg(1);

        // Рисуем "Матрицу совместимости"
        setSvg_x();
        fillSvgX();

        populateA(1);
        populateB(1);

        // Показываем панели совместимости и второй матрицы
        $('#panelX').show(); 
        $('#panel2').show(); 
      }
    }
    else
    {
      // Если первая дата вообще невалидна — покажем panel0 (какой-то блок с сообщением об ошибке)
      $('#panel0').show();
    }
  }

  function pollPaidInterpretation(orderId, maxTries = 120, interval = 3000) {
    console.log("Вызвана pollPaidInterpretation с orderId:", orderId);
    let attempts = 0;
    let waitingMsgId = null;

    function updateWaitingMessage(text) {
      // Удаляем старое сообщение, если оно есть
      if (waitingMsgId) {
        const oldMsg = document.getElementById(waitingMsgId);
        if (oldMsg) oldMsg.remove();
      }
      if (!text) return;
      // Добавляем новое сообщение
      const chatArea = document.querySelector(".chat-area");
      const botMsg = document.createElement("div");
      botMsg.classList.add("message", "bot-message");
      botMsg.textContent = "CHATBOT AI: " + text;
      waitingMsgId = "waiting-msg";
      botMsg.id = waitingMsgId;
      chatArea.appendChild(botMsg);
      chatArea.scrollTop = chatArea.scrollHeight;
    }

    function poll() {
      fetch(`/api/payments/paid-interpretation?order_id=${orderId}`)
        .then(response => response.json())
        .then(data => {
          if (data.message && !data.message.includes("не удалось") && !data.message.includes("Order not paid")) {
            updateWaitingMessage(""); // Удалить индикатор
            // Только ссылка PDF с подписью, без длинного текста интерпретации
            addPdfLink(orderId, "personal");
          } else if (attempts < maxTries) {
            attempts++;
            updateWaitingMessage("Esperando la confirmación del pago..."); // Показываем только один раз
            setTimeout(poll, interval);
          } else {
            updateWaitingMessage(""); // Удалить индикатор
            addBotMessage("No se pudo obtener el resultado de los chakras. Verifique el número de pedido o póngase en contacto con el soporte técnico.");
          }
        })
        .catch(() => {
          if (attempts < maxTries) {
            attempts++;
            updateWaitingMessage("En espera de la confirmación del pago...");
            setTimeout(poll, interval);
          } else {
            updateWaitingMessage("");
            addBotMessage("No se pudo obtener el resultado de los chakras. Verifique el número de pedido o póngase en contacto con el soporte técnico.");
          }
        });
    }
    poll();
  }

  // Функция для получения и отображения результата совместимости
  function fetchCompatibilityResult(orderId) {
    fetch(`/api/payments/compatibility-interpretation?order_id=${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.result) {
                // Только ссылка PDF с подписью, без длинного текста
                addPdfLink(orderId, "compatibility");
            } else if (data.message) {
                openChatWindow("El resultado aún no está listo. Por favor, inténtelo más tarde.");
            } else if (data.error) {
                openChatWindow("Error: " + data.error);
            } else {
                openChatWindow("No se pudo obtener el resultado de la compatibilidad.");
            }
        })
        .catch(error => {
            openChatWindow("Error al obtener el resultado: " + error);
        });
  }

  // Функция для получения и отображения результата персонального анализа
  function fetchPersonalResult(orderId) {
    fetch(`/api/payments/paid-interpretation?order_id=${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.result) {
                // Только ссылка PDF с подписью, без длинного текста
                addPdfLink(orderId, "personal");
            } else if (data.message) {
                openChatWindow("El resultado aún no está listo. Por favor, inténtelo más tarde.");
            } else if (data.error) {
                openChatWindow("Error: " + data.error);
            } else {
                openChatWindow("No se pudo obtener el resultado del análisis personal.");
            }
        })
        .catch(error => {
            openChatWindow("Error al obtener el resultado: " + error);
        });
  }

  function pollCompatibilityResult(orderId, maxTries = 120, interval = 3000) {
    let attempts = 0;
    let waitingMsgId = null;

    function updateWaitingMessage(text) {
      if (waitingMsgId) {
        const oldMsg = document.getElementById(waitingMsgId);
        if (oldMsg) oldMsg.remove();
      }
      if (!text) return;
      const chatArea = document.querySelector(".chat-area");
      const botMsg = document.createElement("div");
      botMsg.classList.add("message", "bot-message");
      botMsg.textContent = "CHATBOT AI: " + text;
      waitingMsgId = "waiting-msg";
      botMsg.id = waitingMsgId;
      chatArea.appendChild(botMsg);
      chatArea.scrollTop = chatArea.scrollHeight;
    }

    function poll() {
      fetch(`/api/payments/compatibility-interpretation?order_id=${orderId}`)
        .then(response => response.json())
        .then(data => {
          if (data.result) {
            updateWaitingMessage("");
            // Только ссылка PDF с подписью, без длинного текста
            addPdfLink(orderId, "compatibility");
          } else if (attempts < maxTries) {
            attempts++;
            updateWaitingMessage("Esperando la confirmación del pago...");
            setTimeout(poll, interval);
          } else {
            updateWaitingMessage("");
            openChatWindow("No se pudo obtener el resultado de la compatibilidad. Verifique el número de pedido o póngase en contacto con el soporte.");
          }
        })
        .catch(() => {
          if (attempts < maxTries) {
            attempts++;
            updateWaitingMessage("En espera de la confirmación del pago...");
            setTimeout(poll, interval);
          } else {
            updateWaitingMessage("");
            openChatWindow("No se pudo obtener el resultado de la compatibilidad. Verifique el número de pedido o póngase en contacto con el soporte.");
          }
        });
    }
    poll();
  }

  // Например, после успешного получения результата:
  localStorage.removeItem("orderId");
  localStorage.removeItem("orderType");