import 'dart:convert';
import 'dart:io';

void main() async {
  final server = await HttpServer.bind('127.0.0.1', 8001);
  print('WebSocket server is running on ws://127.0.0.1:8081');

  await for (HttpRequest request in server) {
    if (request.uri.path == '/ws') {
      final socket = await WebSocketTransformer.upgrade(request);
      print('Client connected');

      socket.listen((message) {
        print('Received message from client: $message');

        // Simulate fetching some information to send back
        final response = {'message': 'Hello from Dart!', 'data': 'Some data'};
        socket.add(jsonEncode(response)); // Send response back as JSON
      });
    } else {
      request.response
        ..statusCode = HttpStatus.forbidden
        ..close();
    }
  }
}
