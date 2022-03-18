# Gateway de comunicação com a api PIX

O Gateway é escrito em Pyhton, usando o framework Flask.

Endpoints disponíveis:

*/qrcode/?id=\<id>:* Este endpoint retorna o QR Code para o identificador (\<id>)
informado;


*/orders/\<id\>/status:* Retorna o estado do pagamento referente ao identificador
(\<id>) informado, 1 para pagamento recebido com sucesso e 0 para um pagamento
não efetuado;

*/webhook/:* Este endpoint é utilizado para receber as notificações do estado do
pagamento enviadas pelo PSP.
