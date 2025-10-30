// This is used to convert units for distances shown

// SCIENCE CENTRE VALUES
// const distanceMetres = 7.5;
// const sameDistancePixels = 72.47068372797375;
const distanceMetres = 248.5 / 100;
const sameDistancePixels = 307;
const distanceMetres2 = 270 / 100;
const sameDistancePixels2 = 287;
// const sameDistancePixels = 290;
export const pixelsToMetresScale1 = distanceMetres / sameDistancePixels;
export const pixelsToMetresScale2 = distanceMetres2 / sameDistancePixels2;
export const pixelsToMetresScale = (pixelsToMetresScale1 + pixelsToMetresScale2) / 2;
