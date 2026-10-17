# iOS Companion

The iOS Companion lets you check Zeus sessions and interact with an active
session from an iPhone or iPad. It is a native SwiftUI app in
[`ios/ZeusCompanion/`](https://github.com/nnayz/zeus/tree/main/ios/ZeusCompanion),
inside this repository.

The app is a client. The Rust Companion gateway runs beside Zeus and remains
the only network entry point. The phone never connects directly to the Zeus
Engine, a PTY, or SSH.

## Availability

The Companion is experimental: it is not distributed through the App Store,
and shipping its production gates is separate work. Building the client,
running a local development gateway, and the API and trust model are
documented in the Developer Guide:
[Companion clients and prototypes](dev/companion-clients.html) and
[Companion architecture and trust model](dev/companion-architecture.html).

The client requires HTTPS. Do not work around this by allowing arbitrary HTTP
or by disabling certificate validation.

## Pair the device

1. Start the Companion gateway on the trusted Mac and create a short-lived
   pairing payload.
2. Copy the complete JSON payload — the app reads it from the clipboard. It has
   this shape:

   ```json
   {
     "origin": "https://zeus.example",
     "server_id": "EXPECTED_SERVER_ID",
     "code": "ONE_TIME_CODE",
     "expires_at_ms": 1790000000000
   }
   ```

3. Open Zeus Companion. If the payload is on the clipboard, the app shows
   **Pairing payload detected**: set the device name (defaults to your device's
   name) and tap **Connect Now**. Otherwise paste the payload under **Manual
   Configuration**, enter a device name, and tap **Pair Device**.
4. Open **Gateway Settings** from the ellipsis menu and check the **Server ID**
   and origin against the trusted computer.

The pairing code expires quickly and is intended for one device. After pairing,
the app stores the bearer token in Keychain. It does not put the token in a URL,
UserDefaults, browser storage, or a WebSocket query string.

## Browse and control a session

After pairing, the app shows the sessions known to Zeus. Select one to load its
current terminal screen.

Type into the message field (**Ask anything or send command…**) and send. If the
session is free, the app acquires the controller lease automatically; you can
also use **Take Control** and **Release Control** from the ellipsis menu to do
it explicitly. **Refresh Screen** reloads the current screen, and **View Raw
Terminal** / **View Document Flow** switch between the raw view and structured
output.

The gateway checks the session identity, control epoch, and command sequence
before the Engine delivers the text to the session. If the lease is stale, the
session changed, or another controller took over, the request fails and the app
reports the error. Refresh the session screen and take control again.

Use **Unpair Device** under **Gateway Settings** when the device should no
longer hold a token. It removes the local Keychain token and disconnects; the
credential on the gateway is not revoked automatically.

## Current boundaries

The app currently supports pairing, session browsing, screen viewing, control
acquisition, and prompt submission. It does not run agents locally, open SSH,
send arbitrary keyboard or mouse events, or act as a replacement for the Zeus
desktop app.

Refresh is currently user initiated. A future client can add the Companion
WebSocket event stream for faster updates, but it must still refetch bounded
state after reconnects and missed events. The phone must be able to reach the
configured HTTPS gateway; background operation and push notifications are not
part of this target.
