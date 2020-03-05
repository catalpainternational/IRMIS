export const tetDaysLocale = {
  name: "tet", // name String
  weekdays: "Domingu_Segunda_Tersa_Kuarta_Kinta_Sexta_Sabadu".split("_"), // weekdays Array
  weekdaysShort: "Dom_Seg_Ter_Kua_Kin_Sex_Sab".split("_"),
  weekdaysMin: "Do_Se_Te_Ku_Ki_Se_Sa".split("_"),
  weekStart: 1,
  months: "Janeiru_Fevereiru_Marsu_Abril_Maiu_Juniu_Juliu_Augustu_Setembru_Outubru_Novembru_Dezembru".split("_"),
  monthsShort: "Jan_Fev_Mar_Abr_Mai_Jun_Jul_Aug_Set_Out_Nov_Dez".split("_"),
  ordinal: n => n + "º", // ordinal Function (number) => return number + output
  formats: {
    // abbreviated format options allowing localization
    LTS: "h:mm:ss A",
    LT: "h:mm A",
    L: "MM/DD/YYYY",
    LL: "MMMM D, YYYY",
    LLL: "MMMM D, YYYY h:mm A",
    LLLL: "dddd, MMMM D, YYYY h:mm A",
    // lowercase/short, optional formats for localization
    l: "D/M/YYYY",
    ll: "D MMM, YYYY",
    lll: "D MMM, YYYY h:mm A",
    llll: "ddd, MMM D, YYYY h:mm A",
  },
  relativeTime: {
    // relative time format strings, keep %s %d as the same
    future: "%s tan", // e.g. in 2 hours, %s been replaced with 2hours
    past: "%s liuba^",
    s: "foin dadaun",
    m: "minuto ida",
    mm: "minuto %d",
    h: "oras ida",
    hh: "oras %d", // e.g. 2 hours, %d been replaced with 2
    d: "loron ida",
    dd: "loron %d",
    M: "fulan ida",
    MM: "fulan %d",
    y: "tinan ida",
    yy: "tinan %d",
  },
  meridiem: (hour, minute, isLowercase) => {
    // OPTIONAL, AM/PM
    return hour > 12 ? "PM" : "AM";
  },
};
