export function isNullOrWhiteSpace(str: string): boolean {
  return str === null || str.replace(/\s/g, "").length < 1;
}

/** Generate an unsigned 32 bit integer hash from any string, such as a featureType name */
export function hashFeatureTypeName(featureType: string): number {
  let hash = 0;

  for (let ix = 0; ix < featureType.length; ix++) {
    const char = featureType.charCodeAt(ix);
    // tslint:disable-next-line
    hash = char + (hash << 6) + (hash << 16) - hash; // magic constant is (effectively) 65599
  }

  const bit32 = Math.pow(2, 32);
  hash = hash < 0 ? Math.ceil(hash) : Math.floor(hash);

  return hash - Math.floor(hash / bit32) * bit32;
}
