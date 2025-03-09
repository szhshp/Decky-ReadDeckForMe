import React from "react";

import { useEffect, useState } from "react";
import {
  ButtonItem,
  PanelSectionRow,
  DropdownItem,
  PanelSection,
  Navigation,
} from "@decky/ui";
import { callable, FileSelectionType, openFilePicker } from "@decky/api";

const download_lang_model = callable<
  [lang: string],
  { status: string; output: string }
>("download_lang_model");

const check_lang_model = callable<
  [lang: string],
  { status: string; output: { [key: string]: boolean } }
>("check_lang_model");

export const Settings = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [lang, setLang] = useState<string>("eng");
  const [loadedLangs, setLoadedLangs] = useState<string[]>([]);
  const [screenshotPath, setScreenshotPath] = useState<string>("");
  const [integrationStatus, setIntegrationStatus] = useState<{
    [key: string]: boolean;
  }>({});

  const openFilePickerHandler = async () => {
    Navigation.CloseSideMenus();

    const res = await openFilePicker(
      FileSelectionType.FOLDER,
      "/home/deck/.local/share/Steam/userdata",
      true,
      undefined,
      undefined,
      undefined,
      false,
      true
    );

    if (res) {
      localStorage.setItem("screenshotPath", res.path);
      setScreenshotPath(res.path);
    }
  };

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

  const download_lang = async () => {
    setLoading(true);
    const result = await download_lang_model(lang);
    console.log(result);
    setLoadedLangs([...loadedLangs, lang]);
    localStorage.setItem("loadedLangs", loadedLangs.join(","));
    setLoading(false);
  };

  const check_model_integration = async () => {
    setLoading(true);
    const result = await check_lang_model(lang);
    setIntegrationStatus(result.output);
    setLoading(false);
  };

  const candidateLangs = [
    { data: "eng", label: "English" },
    { data: "chi_sim", label: "Chinese" },
  ];

  const selectedLang = candidateLangs.find((x) => x.data === lang)?.label;

  const allFilesReady = Object.values(integrationStatus).every(Boolean);

  return (
    <>
      <PanelSection title="Setup Screenshot Path">
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={openFilePickerHandler}
            disabled={loading}
          >
            Select Screenshot Folder
          </ButtonItem>
          <div style={{ fontSize: "10px", overflowWrap: "anywhere" }}>
            <div>Path: {screenshotPath}</div>
            <div>(thumbnails will be excluded)</div>
          </div>
        </PanelSectionRow>
      </PanelSection>
      <PanelSection title="Setup Language">
        <PanelSectionRow>
          <DropdownItem
            label="Language"
            strDefaultLabel={"Language"}
            rgOptions={candidateLangs}
            selectedOption={lang}
            onChange={(val) => {
              setLang(val.data);
              localStorage.setItem("lang", val.data);
            }}
          />
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem layout="below" onClick={download_lang} disabled={loading}>
            Download {selectedLang} Language Data (Approx. 80MB)
          </ButtonItem>
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            onClick={check_model_integration}
            disabled={loading}
          >
            Verify {selectedLang} Language Data Integration
          </ButtonItem>
          {Object.keys(integrationStatus).length > 0 && (
            <div>
              {`${selectedLang} - ${
                Object.values(integrationStatus).filter(Boolean).length
              } of ${Object.keys(integrationStatus).length} Downloaded`}
            </div>
          )}
          {!allFilesReady && (
            <div>
              Click the download button and wait for the download to complete
            </div>
          )}
        </PanelSectionRow>
      </PanelSection>
    </>
  );
};
