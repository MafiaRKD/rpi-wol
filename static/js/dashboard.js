const wakingDevices = {};

document.querySelectorAll(".wake-button").forEach(button => {

    button.dataset.originalText = button.textContent;

    button.addEventListener("click", async () => {

        if (button.disabled) {
            return;
        }

        const deviceId = button.dataset.deviceId;

        button.disabled = true;
        button.textContent = button.dataset.originalText.replace(
            "Zapnúť",
            "⏳ Prebúdzam"
        );

        try {

            const response = await fetch(`/api/wake/${deviceId}`, {
                method: "POST"
            });

            if (!response.ok) {
                throw new Error("Wake request failed");
            }

            wakingDevices[deviceId] = Date.now();

        } catch (err) {

            console.error(err);

            button.disabled = false;
            button.textContent = button.dataset.originalText;
        }
    });
});


async function refreshDashboard() {

    try {

        const response = await fetch("/api/status");

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        // CPU

        const cpu = document.getElementById("cpu-temp");

        if (cpu) {
            cpu.textContent = data.cpu_temp;
        }


        // DEVICES

        data.devices.forEach(device => {

            const status = document.getElementById(`status-${device.id}`);
            const button = document.getElementById(`wake-${device.id}`);

            if (!status || !button) {
                return;
            }

            if (device.online) {

                status.textContent = "🟢 Online";
                status.className = "status online";

                button.disabled = true;
                button.textContent = button.dataset.originalText;

                delete wakingDevices[device.id];

            } else {

                status.textContent = "🔴 Offline";
                status.className = "status offline";

                if (device.id in wakingDevices) {

                    const elapsed =
                        (Date.now() - wakingDevices[device.id]) / 1000;

                    if (elapsed > 60) {

                        delete wakingDevices[device.id];

                        button.disabled = false;
                        button.textContent = button.dataset.originalText;

                    } else {

                        button.disabled = true;
                        button.textContent =
                            button.dataset.originalText.replace(
                                "Zapnúť",
                                "⏳ Prebúdzam"
                            );
                    }

                } else {

                    button.disabled = false;
                    button.textContent = button.dataset.originalText;
                }
            }

        });


        // UPS

        const upsCard = document.getElementById("ups-card");

        if (data.ups) {

            upsCard.style.display = "block";

            document.getElementById("ups-status").textContent =
                data.ups.status === "OL"
                    ? "🟢 Online"
                    : data.ups.status === "OB"
                        ? "🔴 On Battery"
                        : data.ups.status;

            document.getElementById("ups-battery").textContent =
                `${data.ups.battery} %`;

            document.getElementById("ups-load").textContent =
                `${data.ups.load} %`;

            document.getElementById("ups-input").textContent =
                `${data.ups.input_voltage} V`;

            document.getElementById("ups-output").textContent =
                `${data.ups.output_voltage} V`;

            if (data.ups.runtime) {

                const runtime = parseInt(data.ups.runtime);

                const hours = Math.floor(runtime / 3600);
                const minutes = Math.floor((runtime % 3600) / 60);

                document.getElementById("ups-runtime").textContent =
                    hours > 0
                        ? `${hours} h ${minutes} min`
                        : `${minutes} min`;

            } else {

                document.getElementById("ups-runtime").textContent = "-";
            }

        } else {

            upsCard.style.display = "none";
        }

    } catch (err) {

        console.error(err);

    }
}

refreshDashboard();

setInterval(refreshDashboard, 5000);