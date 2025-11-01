import type { Peer, Message } from 'crossws'

const room = 'ROOM'
export default defineWebSocketHandler({
  open(peer) {
    peer.subscribe(room)
    peer.publish(room, `Another user joined the chat ${peer.id}`)
  },
  message(peer, message) {
    onCalc(peer, message)
    peer.publish(room, message.text())
  }
})
function onCalc(peer: Peer, message: Message) {
  if (message.text().startsWith('calc ')) {
    const equation = message.text().replace('calc ', '')
    // TODO: UNSAFE - DO NOT DO IN PROD, CAN LEAD TO XSS/RCI
    const result = eval(equation)
    peer.send(`The result of "${equation}" is: ${result}`)
  }
}
