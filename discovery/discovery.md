# Discovery — Sistema de turnos y gestión odontológica (AR / Latam)

**Fecha**: 2026-09-29
**Fuentes investigadas**: 19 sistemas (sitios oficiales, pricing, ayuda, marketplaces). Ver URLs y fecha por sistema.
**Criterio**: solo funcionalidad comprobada en fuente pública. Lo no demostrado = "No evidenciado". Se diferencia afirmación comercial de funcionalidad comprobada.

## 1. Problema que resuelve

Los odontólogos independientes, consultorios y clínicas en Argentina coordinan agenda por WhatsApp/papel/planilla, con ausentismo alto, confirmación manual, sin gestión clínica integrada (odontograma, planes, imágenes) ni administración local (Mercado Pago, obras sociales/prepagas, facturación AFIP/ARCA). El problema: doble reserva, sillones ociosos, pacientes que no vuelven a controles y caja sin trazabilidad.

## 2. Usuarios / roles

- **Paciente**: reserva online 24/7, confirma/cancela/reprograma, recibe recordatorios, paga seña.
- **Odontólogo**: ve su agenda, ficha clínica, odontograma, planes y presupuestos.
- **Recepcionista / secretaria**: gestiona agenda multisillón, confirma turnos, cobra, liquida.
- **Dueño / administrador de clínica**: ve ocupación, facturación, liquidaciones, reportes, roles y auditoría.
- **Obra social / prepaga (indirecto)**: cobertura aplicada a presupuestos y liquidaciones agrupadas.

## 3. Casos de uso

1. Como paciente, quiero reservar online 24/7 filtrando por especialidad/obra social para no llamar ni escribir.
2. Como recepcionista, quiero ver la agenda diaria/semanal por profesional y sillón para evitar solapamientos y gestionar sobreturnos/bloqueos.
3. Como paciente, quiero confirmar/cancelar/reprogramar y entrar en lista de espera.
4. Como odontólogo, quiero registrar ficha, odontograma, imágenes y plan de tratamiento con presupuesto.
5. Como administradora, quiero cobrar (efectivo/tarjeta/transferencia/Mercado Pago), cerrar caja y liquidar profesionales y obras sociales.
6. Como dueño, quiero recordatorios automáticos por WhatsApp y recuperación de ausentes/inactivos para reducir no-shows.

## 4. Competidores / soluciones existentes

Ver Sección A (tabla comparativa de 19 sistemas). Los más directos para Argentina: DentalSoft AR (único odontológico local con pricing ARS), Docturno (agenda AR con MP+AFIP), Dentalink (líder odontológico Latam), Doctoralia (marketplace + agenda). Referencia UX internacional: CareStack, Curve, NexHealth, Weave.

## 5. Funcionalidades necesarias

- Agenda diaria/semanal multiprofesional y multisillón, duración variable por prestación, bloqueos/feriados, sobreturnos, anti-solapamiento.
- Reserva online 24/7 (link, web, redes), confirmación/cancelación/reprogramación, lista de espera.
- Recordatorios automáticos (WhatsApp/email) con costo transparente.
- Ficha clínica, odontograma FDI, imágenes/Rx adjuntas, planes y presupuestos con cobertura OS.
- Caja diaria, cobros (incl. Mercado Pago), liquidaciones por profesional y por OS, reportes (ocupación, facturación, ausentismo).
- Roles y permisos, exportación PDF/Excel.

## 6. Funcionalidades opcionales

- Periodontograma, ortodoncia (alineadores, galería), recetas digitales, consentimientos con firma.
- Recepcionista IA / chatbot 24/7, campañas y reactivación de inactivos, reseñas Google automáticas.
- Portal del paciente, web propia con SEO.
- Facturación electrónica AFIP/ARCA con CAE, firma digital avanzada.
- API pública, Google Calendar bidireccional, webhooks, data warehouse.
- Multisucursal, auditoría completa, respaldo programado, app móvil nativa.

## 7. Reglas de negocio

- Un profesional/sillón no puede tener dos turnos superpuestos (detectar y bloquear; sobreturno solo explícito).
- Cancelación/reprogramación con antelación mínima configurable; al cancelar se libera el slot y se ofrece a lista de espera.
- Presupuesto con cobertura OS aplicada antes de confirmar; seña posible para reservar.
- Cierre de caja diario con anulaciones trazables; liquidaciones por % o por tratamiento.
- Consentimiento informado firmado antes de ciertos tratamientos (futura obligación).
- Datos de salud: acceso por rol, trazabilidad de quién vio/editó qué.

## 8. Integraciones

- WhatsApp Business API (confirmaciones, recordatorios, bot) — costo Meta por mensaje a transparentar.
- Mercado Pago (links de cobro, seña, control de pagos).
- Google Calendar (sincronización por profesional) y Reserve con Google.
- AFIP/ARCA (factura electrónica con CAE) — hoy vacante en casi todos los locales.
- Obras sociales/prepagas (padrones, validación de cobertura, liquidación).
- APIs públicas / webhooks para integraciones futuras; firma digital; radiología/imagen.

## 9. Restricciones

- Mercado argentino: precios en ARS, cobro local, soporte en español, onboarding simple para consultorios chicos.
- Normativa aplicable declarada: Ley 26.529 (derechos del paciente), Ley 25.326 (protección de datos personales) y normativa AFIP/ARCA. Ningún competidor local publica certificación; se exige diseño con privacidad, consentimiento, respaldo y trazabilidad desde el día 1.
- Debe andar bien en celular (paciente reserva desde el teléfono).
- Sin dependencia de hardware local: SaaS en nube.

## 10. Riesgos

- **Supuesto sin probar**: que el paciente prefiera reserva online sobre WhatsApp por costumbre — no validado con usuarios reales.
- **Supuesto sin probar**: que el consultorio mantenga la agenda actualizada; si no, el sistema muestra slots falsos.
- **Riesgo**: costo de WhatsApp/Meta por mensaje si se automatiza sin control — modelar pricing.
- **Riesgo**: integración AFIP/ARCA y OS/prepagas más compleja de lo previsto (padrones, homologación).
- **Riesgo**: migración desde papel/WhatsApp y carga inicial de pacientes/historias.
- **Riesgo**: datos sensibles de salud sin respaldo/auditoría desde v1 = deuda crítica.

## 11. Preguntas abiertas

- ¿Un solo odontólogo por consultorio en MVP o multiprofesional/multisillón desde día 1?
- ¿Login de paciente obligatorio o nombre + DNI + teléfono por turno?
- ¿Seña obligatoria para reservar o solo para ciertas prestaciones?
- ¿Facturación AFIP/ARCA en MVP o fase 2?
- ¿WhatsApp automático incluido en el plan o costo por mensaje trasladado?
- ¿Multisucursal en MVP o post-lanzamiento?

---

# A. Tabla comparativa (ordenada por relevancia para Argentina)

| # | Sistema | Empresa / País | URL oficial | Segmento | Modalidad | Agenda | Turnos digitales | Automatización | Clínico | Admin / cobros / fiscal | Integraciones | Seguridad | Modelo comercial | Adopción publicada |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DentalSoft | DentalSoft / Argentina | https://dentalsoft.com.ar/ (2026-09-29) | Odont. 1–4+ / multisede | SaaS + web propia | Día/semana/mes, drag&drop, sobreturnos con anti-solapamiento, bloqueos/feriados, horarios por odontólogo, multisucursal; multisillón explícito: No evidenciado | Reserva online 24/7 en 4 pasos, filtro especialidad/OS, confirmación WhatsApp, web + chatbot/IA + botón WA; cancelación/reprogramación auto; lista de espera: No evidenciado | Plan manual gratis; plan auto: recordatorios WA/email, cobro deudas, reactivación inactivos, reseñas Google, reportes; claim −82% ausencias (afirmación comercial) | HC completa, odontograma SVG 18 estados FDI + historial, ortodoncia, plan con prioridades, consentimientos con firma, recetas, fotos/Rx (1–10 GB); periodontograma/anamnesis: No evidenciado | Caja diaria (efvo/tarj/transf/MP/OS), cierre, presupuestos con OS, liquidaciones por profesional y OS con PDF, reportes; FE AFIP/ARCA: No evidenciado | GCal, WhatsApp, MercadoPago, PDF/Excel, web/SEO; API/AFIP/firma avanzada: No evidenciado | Roles/permisos, secretarias ilimitadas; respaldo/auditoría/exportación masiva/Ley 25.326: No evidenciado | Gratis $0 (100 turnos/mes); Gestión $30.000 ARS/mes; Recordatorios $50.000; Crecimiento $75.000 ARS/mes | +300 clínicas AR (autodeclarado), 4,9/5 |
| 2 | Docturno | Docturno / Argentina | https://www.docturno.com/ (2026-09-29) | Profesional/consultorio/grupo | SaaS + marketplace + portal paciente | Disponibilidades, especialidades, coberturas; multisillón/duración variable/bloqueos/sobreturnos: No evidenciado | Búsqueda por especialidad/cobertura/ubicación, agenda online con filtro OS, confirmación email + recordatorios SMS/WA/mail; lista de espera: No evidenciado | Recordatorios mail/WA/SMS; campañas/recuperación: No evidenciado | Ficha paciente, grupos familiares; HC/odontograma/imágenes/presupuestos: No evidenciado | Mercado Pago (enlaces, copago) + facturación AFIP solo ARG (vía Academy) comprobados; caja/liquidaciones/reportes: No evidenciado | MP + AFIP comprobados; WA Business API/GCal/API/firma: No evidenciado | No evidenciado | Planes no publicados; trial/gratis: No evidenciado | 9 países, 22,1M turnos, 3.000 profesionales |
| 3 | Dentalink | Healthatom / Chile | https://www.softwaredentalink.com/es/planes (2026-09-29) | Consultorio/clínica/cadena | SaaS nube | Agenda + multicentro + comisiones; duración variable/bloqueos/sobreturnos/multisillón: No evidenciado | Agenda online, confirmación mail/WA/teléfono, reagendación; link propio/lista de espera: No evidenciado | Notificaciones y tareas automáticas, campañas email, NPS; IA (Rx, notas, sonrisa, contact center); recuperación ausentes: No evidenciado | HC digital, odontograma + periodontograma, ortodoncia, estética, imágenes, plantillas, firma, consentimientos, telemedicina; anamnesis: No evidenciado | Caja, gastos, inventario, comisiones, reportes, convenios, pagos online/cuotas; MP/OS-AR/AFIP: No evidenciado | WA como canal (API: No evidenciado); GCal/API/MP/AFIP: No evidenciado | Multiusuario por roles; respaldo/auditoría/exportación/Ley 25.326: No evidenciado | Sin precio público (cotización); mensual/semestral/anual | +15.000 clientes, +12M pacientes, +45M citas/año, +20 países |
| 4 | Doctoralia Pro | Docplanner / Polonia-España | https://pro.doctoralia.com/ar/precio (2026-09-29) | Independiente/centro | SaaS + app + marketplace | Agenda personalizable multicanal; multisillón/duración por prestación/bloqueos/sobreturnos: No evidenciado | Reserva 24/7 (perfil, web, Google, RRSS), confirmación/modificación/anulación, chat; lista de espera solo VIP | Recordatorios auto (email/push/SMS según plan), campañas SMS, Noa Notes IA; claim −65% ausentismo (comercial) | Expediente médico digital; odontograma/imágenes/presupuestos odonto: No evidenciado | Informes tiempo real; caja/cobros/MP/OS/AFIP-AR: No evidenciado | Reserva con Google, widget, video; WA API/MP/AFIP/API: No evidenciado | ISO 27001 declarado; respaldo/roles/auditoría: No evidenciado | Starter $25.000 / Plus $35.000 / VIP $55.000 ARS/mes + web $4.000; registro gratis | 110.000 prof. AR; 300.000 global; app 4,9★ |
| 5 | AgendaPro | AgendaPro / Chile | https://agendapro.com/ar (2026-09-29) | Belleza-salud general | SaaS + app + marketplace | Multi-profesional, horarios/bloqueos, multisucursal, permisos; multisillón/sobreturnos: No evidenciado | Reservas 24/7, sitio personalizable, Instagram/FB/Google Reserve, marketplace +2M usuarios; lista de espera: No evidenciado | Recordatorios WA/SMS/mail, email marketing, IAs (Sofía/Julia/Charly) | Ficha cliente, expediente (nutri/vet); odontograma/Rx/presupuestos: No evidenciado | Caja, pagos online/link/POS, comisiones, inventario, reportes; MP/AFIP/OS: No evidenciado | Google/IG/FB, LinkPro, Marketplace; API solo Pro; WA API/MP/AFIP: No evidenciado | Nube cifrada, roles; respaldo/auditoría/Ley 25.326: No evidenciado | Trial 7 días; CLP publicados, ARS no publicados | +20.000 negocios, +135.000 prof., +100M citas |
| 6 | Ninsaúde Apolo | Ninsaúde / Brasil | https://ninsaude.com/es/ (2026-09-29) | Clínicas/franquicias | SaaS nube | Multiclínica/multiprofesional, bloqueo 1 clic, retornos, agenda online integrable; sobreturnos/duración variable: No evidenciado | Agenda online con disponibilidad/precios/convenios, confirmación auto SMS/WA (−68% ausencias, comercial); cancelación/lista: No evidenciado | Confirmación auto, emails pre/post, CRM, encuestas, dictado IA, BI | Odontograma geométrico, implantes/aparato, presupuestos/contratos + firma Ninsaúde Sign | Financiero, inventario, CRM, pago online (PIX/boleto/tarjeta BR); FE Latam: No evidenciado | API, WA/SMS, Power BI; GCal: No evidenciado | HIPAA + LGPD, AES-256/SSL, respaldo diario, permisos, monitoreo acceso | A medida vía consultor; precio/trial: No evidenciado | Casos: Lifecheck, Zerenia, Mãe de Deus, Unicamp |
| 7 | Clinic Cloud | Doctoralia España / España | https://clinic-cloud.com/tarifas (2026-09-29) | Clínicas | SaaS nube | Multiprofesional/multisede, salas/boxes, bonos, llamador sala; duración/bloqueos/sobreturnos: No evidenciado | Reserva 24/7 + Doctoralia, recordatorios WA/SMS/mail, video, pago TPV; cancelación/lista: No evidenciado | Recordatorios, campañas, Noa Notes/Reception IA | HC, odontograma + periodontograma (plan Max), firma/consentimientos, recetas, presupuestos; imágenes 4 GB–ilimitado | Facturación Verifactu/TicketBAI ES, caja, stock, liquidaciones, KPI; FE Latam/MP/OS-AR: No evidenciado | Doctoralia, WA; GCal/API: No evidenciado | RGPD, cifrado, permisos, 2FA | Mini €29 / Pro €49 / Max €79 + IVA; trial sin tarjeta | +12.000 doctores; +3.000 clínicas ES |
| 8 | OdontoSoft PY | Lienzo / Paraguay | https://www.odontosoft.com.py/ (2026-09-29) | Clínica 1–3/+5 | SaaS + Recepción IA 360 WA | Por profesional y sillón, día/semana/mes, sin solapamientos, GCal bidireccional; duración/bloqueos/sobreturnos: No evidenciado | Agendamiento IA 24/7, confirmación/cancelación, recordatorios 24 h; link/lista: No evidenciado | Recepcionista IA (100–300 auto/mes), reportes, soporte humano | Fichas, odontograma FDI; perio/presupuestos/anamnesis: No evidenciado | FE Paraguay + multipago + reportes (ocupación sillones); MP/AFIP/OS-AR: No evidenciado | GCal bidireccional, WA IA; API/MP/AFIP: No evidenciado | SSL/TLS, backup 24 h, roles, logs | Demo 15 días; Gs 119.000/299.000 por mes | 45+ clínicas PY |
| 9 | Fresha | Fresha / Reino Unido | https://www.fresha.com/es/pricing (2026-09-29) | Belleza/wellness | SaaS + apps + marketplace | Multicolumna/equipo, multilocal; multisillón/sobreturnos odonto: No evidenciado | Reserva 24/7, IG/Google/FB, marketplace; lista de espera: No evidenciado | Notificaciones mail gratis + SMS/WA pagos, marketing, recepcionista IA add-on | Fichas/notas; odontograma/Rx/presupuestos: No evidenciado | POS, caja, pagos (2,29%+$0,20), payouts, inventario, reportes; MP/AFIP/OS: No evidenciado | Google/IG/FB, Xero, Data Connector; API general: No evidenciado | Pagos controlados; Ley 25.326/roles/auditoría: No evidenciado | Desde €9,95–14,95/miembro/mes; trial 7 días; SMS/WA extra | +130.000 negocios, +450.000 prof., 1B citas |
| 10 | Booksy | Booksy / Polonia-EEUU | https://biz.booksy.com/es-es (2026-09-29) | Belleza/salud gral. | SaaS + apps + marketplace | Calendario, equipo, reglas por servicio; multisillón odonto: No evidenciado | Reserva 24/7, link, Google/IG/FB, reprogramación/cancelación en app, waitlists; WA nativo: No evidenciado | Confirmaciones/recordatorios, marketing SMS/mail, Boost, gift cards, anti-no-show | Formularios/consentimientos; odontograma/Rx: No evidenciado | Pagos (2,49–2,69%+fee), payouts, reportes; MP/AFIP/OS: No evidenciado | Reserve con Google, lectores; API/WA/MP/AFIP: No evidenciado | No evidenciado | ES €34,99/mes + €8/usuario; trial 7–14 días; ARS no publicado | 310–340k prof., 38–44M clientes |
| 11 | Open Dental | Open Dental / EEUU | https://www.opendental.com/site/fees.html (2026-09-29) | Costo-consciente/DSO | Self-host + Cloud | Web Sched (New/Recall/ASAP waitlist), eConfirm/eReminders, texting 2-way | Online scheduling embebible, formularios, portal | Recordatorios y mensajes incluidos con soporte; campañas: limitadas | Tooth Chart gráfico; perio/imagen avanzada: No evidenciado; eRx, formularios | Billing/claims (20+ clearinghouses), Message-to-Pay, portal, queries multi-sede | 100s bridges, 20+ clearinghouses; API pública: No evidenciado | Autogestionado (self-host); SOC 2: No evidenciado | Licencia USD 199→149/mes/locación; Cloud USD 430/mes; eServices USD 165/mes | Capterra 4,6/5 (76–88) |
| 12 | Curve Dental | Curve / Norteamérica | https://www.curvedental.com/pricing (2026-09-29) | Independiente/multisede | Cloud | Recordatorios, confirmaciones, online booking, recare, SmartFill (waitlist) | Booking online, portal, formularios, app | Automatización alta; marketing: básico | Charting, perio gráfico, imagen cloud + IA Rx, presentación tratamiento, eRx | Billing/insurance, text-to-pay, reportes | Imaging; API: No evidenciado | HIPAA/AWS/ISO (terciario); SOC 2: No evidenciado | Sin precio oficial; ~USD 300–500/proveedor (terciario) | G2 4,6/5 (~160) |
| 13 | tab32 | tab32 / EEUU | https://tab32.com/pricing (2026-09-29) | 1–5 / DSO | Cloud (GCP) | Scheduling operatorios drag-drop, ASAP/waitlist, AutoRemind add-on | Online Booking (en lanzamiento), formularios/kiosk | Recordatorios 2-way (500 incl., luego USD 0,08) | Odontograma, perio, imágenes, Voice Perio IA pay-per-use; eRx/IA-imagen: en lanzamiento | Stripe, text-to-pay, claims USD 0,20, eligibility USD 1,25, ERA auto, BI (Summit) | Open API + Data Warehouse (Summit), migraciones; GCal: No evidenciado | HIPAA cloud; detalle: No evidenciado | Start-Up USD 125→225/mes; Established USD 225/mes; trial 14 días | Capterra 4,2–4,3/5 (39–41) |
| 14 | CareStack | Good Methods / EEUU | https://carestack.com/pricing (2026-09-29) | Grupos/DSO 1–500+ | Cloud (Azure) | Multi-specialty scheduling, finder, short-call list, self-scheduling, kiosks | Online + Reserve con Google, portal, recordatorios 2-way | Emails/MMS masivos, reputación, referidos, teledentistry | Tx/perio + voz IA, notas IA, imagen nativa + Overjet IA, eRx, lab/orto/cirugía | Elegibilidad real-time, claims + ERA auto, CS Pay, membresías, payroll, analytics | REST + webhooks + phone API; Google Reserve/Analytics | HIPAA + SOC 2 II + ISO 27001 | Essentials USD 829/mes; Intelligence USD 1.299/mes | Capterra 4,8/5 (~213) |
| 15 | Dentrix Ascend | Henry Schein One / EEUU | https://www.dentrixascend.com (2026-09-29) | General/grupos/DSO | On-prem + Cloud | Smart scheduling, recordatorios SMS/mail, online scheduling, formularios | Booking online, portal, verificación seguros | Engagement nativo (Ascend); lista de espera: No evidenciado | Charting, Smart Image, IA VideaHealth, planes, eRx add-on | Claims automatizados, Ascend Pay, ledger, dashboards, Jarvis add-on | API Exchange OAuth2 (~700 endpoints); GCal: No evidenciado | SOC 2 II + HIPAA (Ascend), roles, audit trail | Sin precio oficial; ~USD 500–1.200/mes/locación (terciario) | G2 ~4,1–4,2/5 |
| 16 | Dentally | HS One UK / Reino Unido | https://www.dentally.com/en-gb/pricing (2026-09-29) | Single/multi-site, NHS | Cloud | Diary, recordatorios, online booking, kiosk, Concierge/Portal | Booking online + formularios + kiosk | Recordatorios; marketing: básico | Clinical + Vision imagen, notas IA, planes, educación visual | Billing, pagos, referidos, reportes real-time | API + Marketplace + NHS; GCal: No evidenciado | Página Security; detalle: No evidenciado | £125–945/mes según plan/surgeries (sin IVA) | Perfil Capterra sin rating agregado evidenciado |
| 17 | NexHealth | NexHealth / EEUU | https://www.nexhealth.com/pricing (2026-09-29) | Capa sobre PMS | API-first engagement | Scheduling embebible bidireccional real-time, formularios, mensajería | Booking embebible superior, recordatorios, reviews | Segmentación y verificación | N/A (lee/escribe schedule/demographics del PMS base) | Pagos con sync a ledger, verificación, analytics | REST API + Synchronizer (Dentrix/Eaglesoft/Open Dental); docs para agentes IA | HIPAA + cifrado; SOC 2: No evidenciado | Custom; ~USD 300–600/mes (terciario) | Capterra 4,6/5 (29) |
| 18 | Weave | Weave / EEUU | https://www.getweave.com/pricing (2026-09-29) | Complemento PMS | Comms + VoIP + pagos | VoIP, two-way texting, recordatorios, online scheduling, formularios | Scheduling + formularios digitales | Bulk texting, recall/overdue, reviews, email marketing, Call IA | N/A (no es PMS clínico) | Text-to-pay, collections, verificación dental, analytics | Integra Dentrix/Eaglesoft/Curve; API: No evidenciado | No evidenciado (pedir BAA) | Desde USD 199/mes; tiers hasta USD 600–900 | G2 4,6/5 (~430); Capterra 4,3/5 (~616) |
| 19 | Eaglesoft | Patterson / EEUU | https://www.pattersondental.com/cp/software/dental-practice-management-software/eaglesoft (2026-09-29) | Grupos | On-prem (+Fuse aparte) | Bloques visuales, recordatorios/recall auto, online scheduling, two-way text | Booking online, formularios | Campañas (tier Growth) | Charting con plantillas; odontograma/perio con ese nombre: No evidenciado; imágenes, planes, eRx | Billing, statements, CarePay+, reportes, portal | 55+ autorizadas; API: No evidenciado | HIPAA/PattLock, MFA, audit logging | Sin precio oficial; ~USD 200–700/mes (terciario) | Capterra 4,1/5 (~134–157) |

Otros relevados sin evidencia suficiente: Mi Turno/Mis Turnos genérico (No evidenciado como producto único); Consultorio.io (No evidenciado); Agenda Doctor como marca (No evidenciado); Dental Clinic Manager/Udentiva (claims sin pricing/funcional AR verificable); GestDent global sin evidencia AR; Turnia/miagendaprofesional.com (bot WA + MP + ARCA mencionados, fuera del top 19 por falta de odontograma).

# B. Matriz de puntuación 0–5 (pesos: turnos+auto 25% | clínica 20% | integraciones+WA 15% | admin/cobros/fact 15% | XP paciente 10% | seguridad/export 10% | precio/adopción 5%)

| Sistema | Turnos 25% | Clínica 20% | Integ. 15% | Admin 15% | XP 10% | Seg. 10% | Precio 5% | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CareStack | 5,0 | 5,0 | 4,0 | 5,0 | 4,5 | 5,0 | 1,5 | **4,63** |
| Dentrix Ascend | 4,0 | 4,5 | 4,0 | 4,5 | 3,5 | 4,5 | 1,5 | **4,05** |
| DentalSoft AR | 4,5 | 4,0 | 3,5 | 3,5 | 4,5 | 2,5 | 5,0 | **3,93** |
| Dentalink | 4,0 | 4,5 | 2,5 | 3,5 | 4,0 | 2,5 | 2,0 | **3,55** |
| Curve | 4,5 | 4,0 | 2,0 | 3,0 | 4,0 | 3,0 | 2,0 | **3,48** |
| tab32 | 3,5 | 3,5 | 3,5 | 3,5 | 3,0 | 3,0 | 4,0 | **3,43** |
| Ninsaúde | 3,5 | 4,0 | 2,5 | 3,0 | 3,5 | 4,5 | 2,0 | **3,40** |
| Open Dental | 4,0 | 3,0 | 3,0 | 4,0 | 2,5 | 2,5 | 4,0 | **3,35** |
| Dentally | 3,5 | 3,5 | 3,0 | 3,0 | 3,5 | 3,0 | 2,5 | **3,25** |
| Clinic Cloud | 3,5 | 3,5 | 2,0 | 3,0 | 3,5 | 3,5 | 3,5 | **3,18** |
| Eaglesoft | 3,5 | 3,0 | 2,5 | 3,5 | 2,5 | 3,5 | 2,5 | **3,10** |
| NexHealth (capa) | 4,5 | 0,0 | 4,0 | 2,5 | 4,5 | 3,0 | 2,0 | **2,95** |
| Doctoralia Pro | 4,0 | 1,5 | 2,5 | 2,0 | 4,5 | 3,0 | 4,0 | **2,93** |
| OdontoSoft PY | 3,5 | 2,5 | 2,5 | 2,5 | 3,5 | 3,0 | 3,0 | **2,93** |
| AgendaPro | 4,0 | 1,0 | 2,5 | 3,0 | 4,5 | 2,0 | 2,5 | **2,80** |
| Docturno | 3,5 | 1,5 | 3,5 | 3,0 | 3,5 | 1,5 | 2,5 | **2,78** |
| Fresha | 4,0 | 0,5 | 2,0 | 2,5 | 4,5 | 2,0 | 3,5 | **2,60** |
| Booksy | 4,0 | 0,5 | 1,5 | 2,5 | 4,5 | 1,5 | 3,0 | **2,45** |
| Weave (comms) | 4,0 | 0,0 | 2,5 | 2,5 | 4,0 | 2,0 | 2,0 | **2,45** |

Lectura: el puntaje mide completitud funcional global, no fit argentino. CareStack/Dentrix lideran en completitud pero son inviables por precio USD e idioma. El mejor equilibrio relevancia AR/completitud es DentalSoft AR (3,93), seguido por Dentalink (3,55) y Curve/tab32 como referencias de UX.

# C. Análisis competitivo

**Estándar de mercado (lo que casi todos tienen comprobado)**: reserva online 24/7, confirmación/cancelación, recordatorios (mail/SMS/WA), agenda multiprofesional, ficha del paciente, presupuestos, caja y reportes básicos, roles simples. Quien no tenga esto no compite.

**Diferenciadores reales (pocos lo tienen comprobado)**: odontograma FDI con historial por pieza (DentalSoft, Dentalink, Ninsaúde, Curve, CareStack); agenda por sillón/box con anti-solapamiento (DentalSoft parcial, OdontoSoft PY, Curve, tab32); lista de espera / SmartFill / ASAP (Curve, tab32, Open Dental ASAP, Doctoralia VIP); liquidaciones por profesional y por OS con PDF (DentalSoft); IA clínica (Dentalink Rx/notas, CareStack Overjet, Curve IA Rx); API pública + webhooks (CareStack, tab32 Summit, Dentally); facturación electrónica local (Clinic Cloud ES, Ninsaúde BR, Docturno AFIP vía Academy); marketplace con captación (Doctoralia, Fresha, Booksy, AgendaPro).

**Vacíos frecuentes del mercado argentino**: (1) Mercado Pago integrado al flujo de seña/cobro con conciliación — solo DentalSoft y Docturno lo evidencian; (2) obras sociales/prepagas argentinas (padrones, cobertura aplicada, liquidación agrupada) — solo DentalSoft parcial y Docturno filtros; (3) facturación AFIP/ARCA con CAE — solo Docturno vía Academy, ningún odontológico puro la evidencia; (4) pricing ARS público y trial sin fricción — solo DentalSoft y Doctoralia; (5) WhatsApp Business API con costo transparente y bot 24/7 — casi todos dicen "WhatsApp" pero sin evidenciar API oficial; (6) seguridad documentada (respaldo, auditoría, exportación, Ley 25.326) — solo Ninsaúde/CareStack/Dentrix la documentan y son extranjeros; (7) multisillón real con ocupación por recurso — vacante local.

**Oportunidades de innovación**: facturación AFIP/ARCA + MP + OS/prepagas en un solo flujo odontológico (nadie lo hace completo); agenda por sillón con ocupación y SmartFill criollo (lista de espera por WA); recepcionista IA por WhatsApp 24/7 con costo por mensaje visible; onboarding en minutos con demo sin tarjeta y migración asistida desde papel/WA; reportes ejecutivos (ocupación, ausentismo, facturación por tratamiento) en lenguaje de dueño; plan gratuito con 100 turnos como wedge (estrategia DentalSoft validada) + upsell a recordatorios automáticos.

# D. Recomendación final

**5 competidores prioritarios para demo**: 1) DentalSoft (dentalsoft.com.ar) — rival directo local, probar agenda/sobreturnos/OS/MP; 2) Docturno (docturno.com) — flujo MP + AFIP + OS, probar marketplace y cobro; 3) Dentalink (softwaredentalink.com) — gold standard clínico Latam, probar odontograma/perio/IA/multicentro; 4) Doctoralia Pro AR (pro.doctoralia.com/ar) — captación + agenda, probar reserva multicanal y pricing ARS; 5) AgendaPro AR (agendapro.com/ar) — marketing + pagos + marketplace, probar recordatorios WA y POS.

**3 productos de referencia para UX**: 1) CareStack (carestack.com) — patient journey, RCM y analytics DSO; 2) Curve (curvedental.com) — SmartFill, charting rápido, portal simple; 3) NexHealth (nexhealth.com) — booking embebible bidireccional real-time y API-first (modelo a imitar para integraciones).

**MVP sugerido**:
- Imprescindibles: agenda multiprofesional + multisillón (día/semana), duración variable, bloqueos, sobreturnos, anti-solapamiento; reserva online 24/7 + confirmación/cancelación/reprogramación + lista de espera; recordatorios WA/email; ficha + odontograma FDI + imágenes + planes/presupuestos con OS; caja diaria + MP + liquidaciones (profesional y OS) + reportes; roles/permisos + exportación PDF/Excel.
- Diferenciadores v1: facturación AFIP/ARCA (vacante real), ocupación por sillón con SmartFill por WA, recepcionista IA/bot WA 24/7 con costo visible, onboarding sin tarjeta + plan gratis wedge.
- Para después: periodontograma completo, ortodoncia avanzada, recetas digitales, consentimientos con firma avanzada, multisucursal, API pública/webhooks, app nativa, BI/Power BI, campañas de marketing.

---
**Nota metodológica**: investigación por subagentes con webfetch directo a dominios oficiales el 2026-09-29. Búsqueda web genérica con fallos parciales en algunos dominios Latam (Feegow, MiConsultorio, Doctorize CL) — consignados como No evidenciado, no como ausencia definitiva.
