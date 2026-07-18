export function buildPatientAccessUrl(origin: string, patientId: string) {
  const normalizedOrigin = origin.endsWith('/') ? origin.slice(0, -1) : origin
  return normalizedOrigin + '/demo/patient/' + encodeURIComponent(patientId)
}
