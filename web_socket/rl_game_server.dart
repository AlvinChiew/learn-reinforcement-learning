import 'dart:convert';
import 'dart:io';

class GameState {
  int position = 0; // Example: simple position-based game

  void reset() {
    position = 0;
  }

  Map<String, dynamic> step(String action) {
    // Simulate action processing (e.g., move forward/backward)
    if (action == "move_forward") position += 1;
    if (action == "move_backward") position -= 1;

    // Return game state and reward
    return {
      "position": position,
      "reward": (position == 10) ? 1 : -0.1,
      "done": position >= 10 || position <= -10,
    };
  }
}

Future<void> main() async {
  final gameState = GameState();

  final server = await HttpServer.bind('localhost', 8080);
  print('WebSocket server listening on ws://localhost:8080');

  await for (HttpRequest request in server) {
    if (WebSocketTransformer.isUpgradeRequest(request)) {
      final websocket = await WebSocketTransformer.upgrade(request);
      websocket.listen((data) {
        final Map<String, dynamic> message = jsonDecode(data);

        if (message["action"] == "reset") {
          gameState.reset();
          websocket.add(jsonEncode(
              {"state": gameState.position, "reward": 0, "done": false}));
        } else if (message["action"] == "step") {
          final result = gameState.step(message["move"]);
          websocket.add(jsonEncode(result));
        }
      });
    }
  }
}
