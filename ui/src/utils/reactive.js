import { isReactive, toRaw } from 'vue'

export function isObject(value) {
  return value !== null && !Array.isArray(value) && typeof value === 'object'
}

export function getRawData(data) {
  return isReactive(data) ? toRaw(data) : data
}

export function isElement(obj) {
  try {
    //Using W3 DOM2 (works for FF, Opera and Chrome)
    return obj instanceof HTMLElement
  } catch (e) {
    //Browsers not supporting W3 DOM2 don't have HTMLElement and
    //an exception is thrown and we end up here. Testing some
    //properties that all elements have (works on IE7)
    return (
      typeof obj === 'object' &&
      obj.nodeType === 1 &&
      typeof obj.style === 'object' &&
      typeof obj.ownerDocument === 'object'
    )
  }
}

export function toDeepRaw(data) {
  const rawData = getRawData(data)

  for (const key in rawData) {
    const value = rawData[key]

    if (!isObject(value) && !Array.isArray(value) && !isElement(value)) {
      continue
    } else {
      console.log(typeof value, value)
      //   break
    }
    rawData[key] = toDeepRaw(value)

    try {
      //   rawData[key] = toDeepRaw(value)
    } catch (err) {
      //   continue
      //   console.warn(typeof value, value)
    }
  }

  return rawData // much better: structuredClone(rawData)
}
