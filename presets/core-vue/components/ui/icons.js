/* Иконки — набор Lucide, а не своя рисовка.

   До этого двадцать два контура были нарисованы вручную прямо в этом файле.
   Так делать нельзя, и вот почему: набор — это не картинки, а система с
   единой сеткой 24, одной толщиной штриха, одинаковыми скруглениями концов
   и общей оптической плотностью. Ручные контуры проваливаются именно там:
   «корона» получилась многоугольником, «волна» — пятью палками, а вес глифа
   гулял от иконки к иконке, потому что сверять его было не с чем.

   Lucide взят не по вкусу, а по трём причинам: сетка 24 и штрих 2 — те же,
   на которые уже рассчитан интерфейс; лицензия ISC (можно всё, включая
   закрытый контур); полторы тысячи глифов, поэтому следующая иконка не
   потребует снова браться за перо. Это же набор по умолчанию у shadcn/ui,
   то есть у той системы, из которой взята и шкала кеглей.

   Импортируются поимённо — сборщик выбрасывает остальные, в бандл попадает
   только то, что перечислено здесь.

   Ключи слева — язык продукта («встреча», «протокол», «волна»), а не имена
   из чужого набора. Поэтому смена набора однажды будет правкой этого файла,
   а не пятидесяти шаблонов. */
import {
  House, Video, FileText, AudioLines, Blocks, User, PanelLeft, ChevronDown,
  ChevronLeft, Globe, Download, Copy, Search, Plus, CircleAlert, Volume2,
  LayoutGrid, Check, X, Info, Crown, Contrast, Rows3, EllipsisVertical,
  CircleDot, RefreshCw, ChevronsUpDown, ArrowUp, ArrowDown, Minus, Folder, FolderInput,
  Calendar, Eye, EyeOff, Mail,
} from 'lucide-vue-next'

export const icons = {
  home: House,
  video: Video,          /* встреча */
  doc: FileText,         /* протокол, шаблон */
  wave: AudioLines,      /* голос — центральный знак продукта */
  plug: Blocks,          /* интеграции: кубики собираются, вилка — про питание */
  user: User,
  panel: PanelLeft,      /* свернуть сайдбар */
  chevron: ChevronDown,
  back: ChevronLeft,
  globe: Globe,
  download: Download,
  copy: Copy,
  search: Search,
  plus: Plus,
  alert: CircleAlert,
  volume: Volume2,
  grid: LayoutGrid,
  check: Check,
  close: X,
  info: Info,
  crown: Crown,          /* тариф */
  theme: Contrast,       /* тема */
  rows: Rows3,           /* плотность */
  more: EllipsisVertical, /* остальные действия */
  live: CircleDot,        /* идёт запись */
  sync: RefreshCw,        /* обработка, повтор */
  sort: ChevronsUpDown,   /* колонка сортируется, но не выбрана */
  up: ArrowUp,
  down: ArrowDown,
  minus: Minus,           /* выбрана часть строк */
  folder: Folder,
  'folder-move': FolderInput, /* переложить в папку */
  calendar: Calendar,
  mail: Mail,
  eye: Eye,
  'eye-off': EyeOff,
}
