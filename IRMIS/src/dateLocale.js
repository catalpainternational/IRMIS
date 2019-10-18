import dayjs from 'dayjs'
import pt from 'dayjs/locale/pt'
import { tetDaysLocale} from './locale/dayjs_tet'

// Known locales
const dayJsLocales = {
    'tet': tetDaysLocale,
    'pt': pt
};

// set locale from window language code
const dayJsLocale = dayJsLocales[window.language_code]; 
if (dayJsLocale !== undefined) {
    dayjs.locale(dayJsLocale);
}
