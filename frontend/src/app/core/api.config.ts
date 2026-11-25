import { Capacitor } from '@capacitor/core';

const PUERTO = 8000;

/**
 * Para un teléfono real, escribe aquí la IPv4 de tu PC (ipconfig), por ejemplo '192.168.1.50',
 * y añádela también a ALLOWED_HOSTS en backend/.env. Déjalo vacío para el emulador.
 */
const IP_TELEFONO_REAL = '';

/** Dirección base de la API según dónde se ejecute la app. */
export function urlApi(): string {
  if (Capacitor.getPlatform() === 'android') {
    // El emulador llega a la PC con 10.0.2.2; un teléfono real, con la IP de la PC.
    return `http://${IP_TELEFONO_REAL || '10.0.2.2'}:${PUERTO}/api`;
  }
  // Navegador de la PC con ng serve: el proxy (proxy.conf.json) reenvía /api al backend.
  if (location.port === '8100' || location.port === '4200') {
    return '/api';
  }
  // Navegador de la PC (otros casos).
  return `http://127.0.0.1:${PUERTO}/api`;
}
