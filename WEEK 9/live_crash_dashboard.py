import serial
import time
from collections import deque
import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

SERIAL_PORT = "/dev/cu.usbmodem13201"  
BAUD_RATE = 115200
MAX_POINTS = 100
CRASH_HOLD_CYCLES = 5  

x_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
y_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
z_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
crash_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
timestamps = deque([datetime.datetime.now()]*MAX_POINTS, maxlen=MAX_POINTS)
crash_hold_counter = 0

# Communication config
SENDER_EMAIL = "ayushjainn42@gmail.com"
RECEIVER_EMAIL = "evaayush42s@gmail.com@gmail.com"
EMAIL_PASSWORD = "evaayush10"  


TWILIO_SID = 'ymeinhoonayush'
TWILIO_AUTH_TOKEN = '543-7A3-56832'
TWILIO_PHONE = '+0478625790 
EMERGENCY_CONTACT = '0456783590'  
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


def serial_reader():
    global crash_hold_counter
    ser = None
    while ser is None:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"onnected to {SERIAL_PORT}")
        except serial.SerialException:
            print(f"Cannot open {SERIAL_PORT}. Retrying in 2s...")
            time.sleep(2)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            vals = line.split(',')
            if len(vals) != 4:
                print("Bad line:", line)
                continue

            ax, ay, az, crash = map(float, vals)
            x_data.append(ax)
            y_data.append(ay)
            z_data.append(az)

            # Hold crash in Python for a few cycles
            if crash >= 1:
                crash_hold_counter = CRASH_HOLD_CYCLES

            if crash_hold_counter > 0:
                crash_data.append(1)
                crash_hold_counter -= 1
            else:
                crash_data.append(0)

            timestamps.append(datetime.datetime.now())

        except Exception as e:
            print("Serial error:", e)
            time.sleep(0.5)

threading.Thread(target=serial_reader, daemon=True).start()


def send_email_alert():
    msg = MIMEText(" Crash detected! Check your dashboard immediately.")
    msg['Subject'] = "CRASH ALERT"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print(" Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

def alert_emergency():
    try:
        # Send SMS
        sms = twilio_client.messages.create(
            body=" Crash detected! Immediate assistance required!",
            from_=TWILIO_PHONE,
            to=EMERGENCY_CONTACT
        )
        print(f"SMS sent: {sms.sid}")

    
        call = twilio_client.calls.create(
            twiml='<Response><Say>Emergency! A crash has been detected. Please respond immediately.</Say></Response>',
            from_=TWILIO_PHONE,
            to=EMERGENCY_CONTACT
        )
        print(f"Call initiated: {call.sid}")

        # Send backup email
        send_email_alert()

    except Exception as e:
        print("Emergency alert failed:", e)


app = dash.Dash(__name__)
app.title = "Live Crash Detection Dashboard"

app.layout = html.Div([
    html.H1("Live Crash Detection Dashboard", style={'text-align':'center'}),
    dcc.Graph(id='accel-graph'),
    dcc.Graph(id='crash-graph'),
    dcc.Interval(
        id='interval-component',
        interval=200,  
        n_intervals=0
    ),
    html.Div(id='live-g', style={'font-size':24, 'text-align':'center', 'margin-top':20})
])


@app.callback(
    [Output('accel-graph', 'figure'),
     Output('crash-graph', 'figure'),
     Output('live-g', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    latest_crash = max(list(crash_data)[-5:]) if len(crash_data) > 0 else 0
    crash_triggered = latest_crash >= 1

    # Accelerometer Graph
    accel_fig = go.Figure()
    accel_fig.add_trace(go.Scatter(y=list(x_data), mode='lines+markers', name='X', line=dict(color='blue')))
    accel_fig.add_trace(go.Scatter(y=list(y_data), mode='lines+markers', name='Y', line=dict(color='green')))
    accel_fig.add_trace(go.Scatter(y=list(z_data), mode='lines+markers', name='Z', line=dict(color='orange')))
    accel_fig.update_layout(title='Accelerometer (m/s²)', yaxis=dict(range=[-5, 5]))

    # Crash Gauge
    crash_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_crash,
        title={'text': "Crash Detection"},
        gauge={
            'axis': {'range': [0, 1]},
            'steps': [
                {'range': [0, 0.5], 'color': "lightgreen"},
                {'range': [0.5, 1], 'color': "red"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 1}
        }
    ))

    # Emergency alert (SMS, call, email)
    if crash_triggered and not hasattr(update_graph, 'notified'):
        alert_emergency()
        update_graph.notified = True
    elif not crash_triggered:
        update_graph.notified = False

    # Live g-force
    if len(x_data) > 0:
        g_force = ((x_data[-1]**2 + y_data[-1]**2 + z_data[-1]**2)**0.5) / 9.81
        g_text = f"Current g-force: {g_force:.2f} g {'⚠️ CRASH DETECTED!' if crash_triggered else ''}"
    else:
        g_text = "Waiting for data..."

    return accel_fig, crash_fig, g_text


if __name__ == '__main__':
    app.run(debug=True, port=8051)
