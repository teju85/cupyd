;; show line and column numbers in modeline
(setq line-number-mode t)
(setq column-number-mode t)
;; settings which makes the emacs session to be easier and user-friendly
(setq case-fold-search t)
(global-font-lock-mode t)
(setq indent-tabs-mode nil)
(show-paren-mode t)
(blink-cursor-mode t)
(setq inhibit-startup-message t)
(setq initial-scratch-message "")
;; save the precious screen real estate!
(menu-bar-mode -1)
;; page scrolling in line-by-line fashion
(setq scroll-step 1)
;; default settings for language and input methods
(setq current-language-environment "English")
(setq default-input-method "latin-1-prefix")
;; overwrite selected text
(delete-selection-mode t)
;; DO NOT use tabs for indentation (definition of tabs vary for every editor!)
(setq-default indent-tabs-mode nil)
;; disable creating backup files!
(setq make-backup-files nil)
;; dired enable reuse of buffers through command 'a'
(put 'dired-find-alternate-file 'disabled nil)
;; short answers are preferred!
(fset 'yes-or-no-p 'y-or-n-p)
;; have emacs show tooltips in echo area instead of a separate frame
(tooltip-mode nil)
;; keep quiet, please!!
(setq visible-bell nil)
(setq ring-bell-function #'ignore)
;; trailing whitespaces
(setq show-trailing-whitespace t)

;; trigger indentation on a few keystrokes
(electric-indent-mode 1)

;; lage file warning threshold (30MB)
(setq large-file-warning-threshold 30000000)

;; modes based on file extensions
(add-to-list 'auto-mode-alist '("\\.el\\'" . emacs-lisp-mode))
(add-to-list 'auto-mode-alist '("\\.h\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.c\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.cc\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.cu\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.cuh\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.cpp\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.hpp\\'" . c++-mode))
(add-to-list 'auto-mode-alist '("\\.t\\'" . perl-mode))
(add-to-list 'auto-mode-alist '("\\.tl\\'" . perl-mode))
(add-to-list 'auto-mode-alist '("\\.pl\\'" . perl-mode))
(add-to-list 'auto-mode-alist '("\\.pm\\'" . perl-mode))
(add-to-list 'auto-mode-alist '("\\.py\\'" . python-mode))
(add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))
(add-to-list 'auto-mode-alist '("CMakeLists\\.txt\\'" . cmake-mode))
(add-to-list 'auto-mode-alist '("\\.cmake\\'" . cmake-mode))
(add-to-list 'auto-mode-alist '("\\.pdf\\'" . doc-view-mode))

(global-unset-key "\C-f")
(global-unset-key "\C-q")
(global-set-key "\C-f\C-s" 'replace-string)
(global-set-key (kbd "M-g") 'goto-line)

;; buffer management
(global-set-key (kbd "<f12>") 'quoted-insert)
(global-set-key "\C-q\C-t" 'kill-this-buffer)
;; it is easy to hit C-x C-c, so avoid unintentional exits
(global-set-key "\C-q\C-e" 'save-buffers-kill-emacs)
