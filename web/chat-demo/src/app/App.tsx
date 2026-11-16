import { useEffect, useState } from 'react'
import { useTranslate } from '../i18n/index.js'
import { useSettings } from '../services/settings.js'
import { useIsMobile, useMobileViewport, usePreventPageScroll } from './viewport.js'
import {
  bindChatPersistence,
  initChat,
  retrySaveSessions,
  selectSession,
  useChatStore,
} from '../services/chat/store.js'
import { SearchPanel } from '../components/search/SearchPanel.js'
import { closeSearchPanel } from '../components/search/searchPanelState.js'
import { SessionView } from '../components/session/SessionView.js'
import { MobileHeader } from '../components/session/MobileHeader.js'
import { Welcome } from '../components/session/Welcome.js'
import { ensureApiKey } from '../components/settings/settingsDialogState.js'
import { SettingsDialog } from '../components/settings/SettingsDialog.js'
import { Toast } from '../components/base/Toast.js'
import { showToast } from '../components/base/toastState.js'
import { onUploadNotice } from '../services/attachments.js'
import { Button } from '../components/base/Button.js'
import { stopReadAloud } from '../services/speech/readAloud.js'
import { CollapsedSider } from '../components/sider/CollapsedSider.js'
import { closeMobileSider } from '../components/sider/mobileSiderState.js'
import { MobileSider, Sider } from '../components/sider/Sider.js'
import { MiniHouse3DSimulator } from '../components/minihouse/MiniHouse3DSimulator.js'
import {
  MiniHouseDocumentaryContent,
  prefillAiQuestion,
  TopNavigationHeader,
  type WorkspaceViewMode,
} from '../components/minihouse/MiniHouseFrontPage.js'
import styles from './App.module.css'

export const App = () => {
  const t = useTranslate()
  const isMobile = useIsMobile()
  const locale = useSettings((state) => state.locale)
  // 移动端侧边栏以独立抽屉管理开合状态
  const siderCollapsed = useSettings((state) => state.siderCollapsed) && !isMobile
  const ready = useChatStore((state) => state.ready)
  const initError = useChatStore((state) => state.initError)
  const saveError = useChatStore((state) => Object.values(state.sessionSaveErrors).some(Boolean))
  const importingHistory = useChatStore((state) => state.importingHistory)
  const session = useChatStore((state) =>
    state.activeId !== null && Object.hasOwn(state.sessionCache, state.activeId)
      ? state.sessionCache[state.activeId]
      : undefined
  )
  const sessionLoadError = useChatStore((state) =>
    state.activeId === null ? false : state.sessionLoadErrors[state.activeId] === true
  )
  const frameRef = useMobileViewport(isMobile)
  const streaming = useChatStore((state) =>
    state.activeId === null ? false : Object.hasOwn(state.streaming, state.activeId)
  )
  const activeId = useChatStore((state) => state.activeId)
  const [viewMode, setViewMode] = useState<WorkspaceViewMode>('overview')
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false)

  usePreventPageScroll(isMobile && viewMode === 'chat')

  useEffect(() => {
    document.documentElement.lang = locale
  }, [locale])

  // 文件数、存储空间达到上限时，附件上只显示「上传失败」，原因用 toast 说明
  useEffect(() => onUploadNotice(showToast), [])
  useEffect(bindChatPersistence, [])

  // 搜索结果面板只属于当前会话
  useEffect(closeSearchPanel, [activeId])
  // 切换会话时停止朗读
  useEffect(stopReadAloud, [activeId])
  // 移动端选中会话、切换布局后收起抽屉
  useEffect(closeMobileSider, [activeId, isMobile])

  useEffect(() => {
    void initChat()
  }, [])

  const handleAskAi = (prompt: string) => {
    prefillAiQuestion(prompt)
    if (viewMode === 'overview') {
      setDrawerOpen(true)
    }
    ensureApiKey()
  }

  const chatPane = (
    <main className={styles.main}>
      {saveError ? (
        <div className={styles.saveError} role="alert">
          <span>{t('sessionSaveFailed')}</span>
          <Button
            variant="outlined"
            size="s"
            disabled={importingHistory}
            onClick={retrySaveSessions}
          >
            {t('retry')}
          </Button>
        </div>
      ) : null}
      <div className={styles.content}>
        {viewMode === 'chat' && siderCollapsed ? <CollapsedSider /> : null}
        {!ready || (activeId !== null && !session) ? (
          <div className={styles.loadingView}>
            {isMobile ? <MobileHeader /> : null}
            <div className={styles.loadingState} role="status" aria-live="polite">
              <span>
                {(!ready ? initError : sessionLoadError)
                  ? t(!ready ? 'sessionListLoadFailed' : 'sessionLoadFailed')
                  : t('sessionLoading')}
              </span>
              {(!ready ? initError : sessionLoadError) ? (
                <Button
                  variant="outlined"
                  size="m"
                  onClick={() => {
                    if (!ready) {
                      void initChat()
                    } else if (activeId !== null) {
                      selectSession(activeId)
                    }
                  }}
                >
                  {t('retry')}
                </Button>
              ) : null}
            </div>
          </div>
        ) : session ? (
          <SessionView
            session={session}
            streaming={streaming}
            siderCollapsed={viewMode !== 'chat' || siderCollapsed}
          />
        ) : (
          <Welcome />
        )}
      </div>
    </main>
  )

  return (
    <>
      <div
        ref={frameRef}
        style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', overflow: 'hidden' }}
      >
        <TopNavigationHeader
          viewMode={viewMode}
          setViewMode={(mode) => {
            setViewMode(mode)
            if (mode === 'chat') {
              ensureApiKey()
            }
          }}
          drawerOpen={drawerOpen}
          setDrawerOpen={(open) => {
            setDrawerOpen(open)
            if (open) {
              ensureApiKey()
            }
          }}
        />

        {viewMode === 'overview' ? (
          <div style={{ display: 'flex', flex: 1, minHeight: 0, position: 'relative' }}>
            <MiniHouseDocumentaryContent onAskAi={handleAskAi} />
            {drawerOpen ? (
              <aside
                aria-label="OpenRouter Free AI Assistant Drawer"
                style={{
                  width: isMobile ? '100%' : '460px',
                  borderLeft: '1px solid #CBD5E1',
                  display: 'flex',
                  flexDirection: 'column',
                  background: 'var(--dsw-alias-bg-base)',
                  boxShadow: '-12px 0 32px rgba(0,0,0,0.15)',
                  zIndex: 30,
                }}
              >
                {chatPane}
              </aside>
            ) : null}
          </div>
        ) : viewMode === 'split' ? (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: isMobile ? '1fr' : '1.25fr 0.95fr',
              flex: 1,
              minHeight: 0,
              background: '#0D1117',
            }}
          >
            <div style={{ overflowY: 'auto', padding: '18px' }}>
              <MiniHouse3DSimulator onAskAi={handleAskAi} />
            </div>
            <div
              style={{
                borderLeft: '1px solid #262F3D',
                display: 'flex',
                minHeight: 0,
                overflow: 'hidden',
                background: 'var(--dsw-alias-bg-base)',
              }}
            >
              {chatPane}
            </div>
          </div>
        ) : (
          <div className={styles.frame} style={{ position: 'relative', flex: 1, minHeight: 0 }}>
            {isMobile ? <MobileSider /> : siderCollapsed ? null : <Sider />}
            {chatPane}
            <SearchPanel />
          </div>
        )}
      </div>
      <SettingsDialog />
      <Toast />
    </>
  )
}
