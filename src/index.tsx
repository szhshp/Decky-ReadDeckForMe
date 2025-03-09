/* eslint-disable react/react-in-jsx-scope */
import {
  addEventListener,
  callable,
  definePlugin,
  FileSelectionType,
  openFilePicker,
  removeEventListener,
  routerHook,
  toaster,
} from "@decky/api";
import {
  ButtonItem,
  DropdownItem,
  Navigation,
  PanelSection,
  PanelSectionRow,
  SidebarNavigation,
  staticClasses,
} from "@decky/ui";
import { useEffect, useState } from "react";
import { FaFolder, FaShip, FaTrashAlt, FaVolumeUp } from "react-icons/fa";
import { Settings } from "./pages/Settings";

const ocr_latest = callable<
  [path: string, lang: string],
  { status: string; output: string }
>("ocr_latest");

const get_latest = callable<
  [path: string],
  { status: string; output: string; base64: string }
>("get_latest");

const download_lang_model = callable<
  [lang: string],
  { status: string; output: string }
>("download_lang_model");

const check_lang_model = callable<
  [lang: string],
  { status: string; output: { [key: string]: boolean } }
>("check_lang_model");

const delete_latest = callable<
  [path: string],
  { status: string; output: string }
>("delete_latest");

const Content = () => {
  const [content, setContent] = useState<string | undefined>();
  const [loading, setLoading] = useState<boolean>(false);
  const [lang, setLang] = useState<string>("eng");
  const [loadedLangs, setLoadedLangs] = useState<string[]>([]);
  console.log("loadedLangs: ", loadedLangs);
  const [screenshotPath, setScreenshotPath] = useState<string>("");
  // const [integrationStatus, setIntegrationStatus] = useState<{
  //   [key: string]: boolean;
  // }>({});

  useEffect(() => {
    const onInit = async () => {
      setScreenshotPath(
        localStorage.getItem("screenshotPath") ||
          "/home/deck/.local/share/Steam/userdata"
      );
      setLang(localStorage.getItem("lang") || "eng");
      setLoadedLangs(localStorage.getItem("loadedLangs")?.split(",") || []);
    };
    onInit();
  }, []);

  const get_latest_img = async () => {
    setLoading(true);
    const result = await get_latest(screenshotPath);
    setContent(result.base64);
    setLoading(false);
  };

  const ocr = async () => {
    console.log("ocr");
    setLoading(true);
    await ocr_latest(screenshotPath, lang);
    setLoading(false);
  };

  const delete_latest_img = async () => {
    setLoading(true);
    const result = await delete_latest(screenshotPath);
    console.log(result);
    setContent(undefined);
    setLoading(false);
  };

  // const download_lang = async () => {
  //   setLoading(true);
  //   const result = await download_lang_model(lang);
  //   console.log(result);
  //   setLoadedLangs([...loadedLangs, lang]);
  //   localStorage.setItem("loadedLangs", loadedLangs.join(","));
  //   setLoading(false);
  // };

  // const check_model_integration = async () => {
  //   setLoading(true);
  //   const result = await check_lang_model(lang);
  //   setIntegrationStatus(result.output);
  //   setLoading(false);
  // };

  // const candidateLangs = [
  //   { data: "eng", label: "English" },
  //   { data: "chi_sim", label: "Chinese" },
  // ];

  // const selectedLang = candidateLangs.find((x) => x.data === lang)?.label;

  return (
    <>
      <PanelSection title="Configuration">
        <PanelSectionRow>
          <div style={{ fontSize: "10px", overflowWrap: "anywhere" }}>
            Please check the configuration before using the actions below.
          </div>
          <ButtonItem
            layout="below"
            onClick={() => {
              Navigation.Navigate("/rifm-config");
              Navigation.CloseSideMenus();
            }}
          >
            Language Settings
          </ButtonItem>
        </PanelSectionRow>
      </PanelSection>
      <PanelSection title="Actions">
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={get_latest_img}
            disabled={loading}
          >
            <FaFolder style={{ paddingRight: "4px" }} />
            {loading ? "Loading..." : "Get Latest File"}
          </ButtonItem>
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem layout="below" onClick={ocr} disabled={loading}>
            <FaVolumeUp style={{ paddingRight: "4px" }} />
            {loading ? "Loading..." : "Read Deck For Me"}
          </ButtonItem>
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={delete_latest_img}
            disabled={loading}
          >
            <FaTrashAlt style={{ paddingRight: "4px" }} />
            {loading ? "Loading..." : "Delete Latest File"}
          </ButtonItem>
        </PanelSectionRow>

        {content && (
          <PanelSectionRow>
            <div style={{ display: "flex", justifyContent: "center" }}>
              <img
                src={`data:image/png;base64,${content}`}
                alt="OCR Result"
                style={{ width: "80vw", border: "1px solid grey" }}
              />
            </div>
          </PanelSectionRow>
        )}
      </PanelSection>
    </>
  );
};

const DeckyPluginRouterTest = () => {
  return (
    <SidebarNavigation
      title="ReadDeckForMe"
      showTitle
      pages={[
        {
          title: "Settings",
          content: <Settings />,
          route: "/rifm-config/settings",
        },
      ]}
    />
  );
};

export default definePlugin(() => {
  console.log(
    "Template plugin initializing, this is called once on frontend startup"
  );

  // Add an event listener to the "toast_event" event from the backend
  const listener = addEventListener<[test1: string]>("toast_event", (test1) => {
    console.log("Template got toast_event with:", test1);
    toaster.toast({
      title: "Notification From RIFM",
      body: `${test1}`,
    });
  });

  routerHook.addRoute("/rifm-config", DeckyPluginRouterTest, {
    exact: true,
  });

  return {
    // The name shown in various decky menus
    name: "Decky-ReadDeckForMe",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>Read Deck For Me</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <FaShip />,
    // The function triggered when your plugin unloads
    onDismount() {
      console.log("Unloading");
      removeEventListener("toast_event", listener);
      routerHook.removeRoute("/rifm-config");
    },
  };
});
