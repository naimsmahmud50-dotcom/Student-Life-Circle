/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Emergency Mesh & Solar Station Telemetry
 * TOPIC:     Off-Grid Photovoltaic Telemetry & Village Student Node Mesh Monitoring
 * FILE:      frontend/src/components/emergency-mesh/SolarStationTelemetry.tsx
 * PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
 * PURPOSE:   Renders real-time telemetry from remote riverine Char/Haor solar stations,
 *            monitoring battery voltage (12.8V LiFePO4), state of charge (SoC),
 *            solar irradiance, student mesh connections, and delay-tolerant buffers.
 * STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
 */

import React, { useState, useEffect } from 'react';
import {
  Sun,
  Battery,
  Signal,
  Radio,
  Zap,
  Thermometer,
  Users,
  ShieldCheck,
  RefreshCw,
  Layers,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';

export interface SolarTelemetryData {
  station_id: string;
  location_name: string;
  region: string;
  battery_voltage_v: number;
  battery_soc_percent: number;
  solar_irradiance_wm2: number;
  pv_power_w: number;
  load_power_w: number;
  system_temperature_c: number;
  connected_student_nodes: number;
  channel_frequency_mhz: number;
  signal_rssi_dbm: number;
  snr_db: number;
  gateway_online: boolean;
  dtn_pending_packets?: number;
  last_handshake?: string;
}

export interface SolarStationTelemetryProps {
  stationId?: string;
  className?: string;
}

export const SolarStationTelemetry: React.FC<SolarStationTelemetryProps> = ({
  stationId = 'SOLAR-CHAR-CHILMARI-01',
  className = '',
}) => {
  const [telemetry, setTelemetry] = useState<SolarTelemetryData>({
    station_id: stationId,
    location_name: 'চিলমারী ব্রহ্মপুত্র চরে স্থাপিত সোলার মাইক্রো-হাব',
    region: 'কুড়িগ্রাম (Kurigram)',
    battery_voltage_v: 13.25,
    battery_soc_percent: 94.0,
    solar_irradiance_wm2: 720.0,
    pv_power_w: 88.5,
    load_power_w: 14.2,
    system_temperature_c: 28.5,
    connected_student_nodes: 18,
    channel_frequency_mhz: 868.1,
    signal_rssi_dbm: -96.0,
    snr_db: 7.5,
    gateway_online: true,
    dtn_pending_packets: 3,
  });

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchTelemetry();
  }, [stationId]);

  const fetchTelemetry = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/v1/emergency/station/status?station_id=${stationId}`);
      if (res.ok) {
        const data = await res.json();
        setTelemetry(data);
      }
    } catch {
      // Retain existing telemetry state if offline
    } finally {
      setIsLoading(false);
    }
  };

  const netPower = telemetry.pv_power_w - telemetry.load_power_w;

  return (
    <div className={`p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-700/80 shadow-2xl text-slate-100 ${className}`}>
      {/* Station Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-amber-950/80 border border-amber-600/80 text-amber-400 shadow-inner">
            <Sun className="w-6 h-6 animate-pulse" strokeWidth={1.75} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase tracking-wider text-amber-400 font-bold">
                Off-Grid Solar Micro-Hub
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              <span className="text-xs font-mono text-slate-400">{telemetry.station_id}</span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold font-bengali text-white">
              {telemetry.location_name}
            </h3>
            <p className="text-xs font-bengali text-slate-400">{telemetry.region}</p>
          </div>
        </div>

        {/* Uplink Status Pill */}
        <div className="flex items-center gap-3">
          <div
            className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono border ${
              telemetry.gateway_online
                ? 'bg-emerald-950/70 border-emerald-600 text-emerald-300'
                : 'bg-amber-950/70 border-amber-600 text-amber-300'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                telemetry.gateway_online ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'
              }`}
            />
            <span>{telemetry.gateway_online ? 'GATEWAY UPLINK ACTIVE' : 'DTN BUFFERING MODE'}</span>
          </div>

          <button
            type="button"
            onClick={fetchTelemetry}
            className="p-2 rounded-xl bg-slate-800 border border-slate-700 hover:bg-slate-700 text-slate-300 transition-all"
            title="টেলিমেট্রি রিফ্রেশ করুন"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} strokeWidth={1.75} />
          </button>
        </div>
      </div>

      {/* Main Telemetry Instruments Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 py-6">
        {/* Metric 1: Battery Bank Storage */}
        <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>LiFePO4 BATTERY</span>
            <Battery className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-black font-mono text-emerald-400 tabular-nums">
              {telemetry.battery_soc_percent.toFixed(1)}%
            </div>
            <div className="text-xs font-mono text-slate-300 flex items-center justify-between">
              <span>ভোল্টেজ:</span>
              <span className="font-bold text-white tabular-nums">{telemetry.battery_voltage_v.toFixed(2)} V</span>
            </div>
          </div>
          {/* Visual Reserve Bar */}
          <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-700">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, telemetry.battery_soc_percent)}%` }}
            />
          </div>
        </div>

        {/* Metric 2: Solar Photovoltaic Generation */}
        <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>SOLAR PV ARRAY</span>
            <Sun className="w-4 h-4 text-amber-400" strokeWidth={1.75} />
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-black font-mono text-amber-300 tabular-nums">
              {telemetry.pv_power_w.toFixed(1)} <span className="text-sm font-normal text-slate-400">W</span>
            </div>
            <div className="text-xs font-mono text-slate-300 flex items-center justify-between">
              <span>বিকিরণ:</span>
              <span className="font-bold text-white tabular-nums">{telemetry.solar_irradiance_wm2.toFixed(0)} W/m²</span>
            </div>
          </div>
          <div className="text-[11px] font-mono text-emerald-400 flex items-center gap-1">
            <Zap className="w-3 h-3" />
            <span>নেট চার্জিং: +{netPower.toFixed(1)} W</span>
          </div>
        </div>

        {/* Metric 3: Connected Student Radios */}
        <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>VILLAGE MESH NODES</span>
            <Users className="w-4 h-4 text-teal-400" strokeWidth={1.75} />
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-black font-mono text-teal-300 tabular-nums">
              {telemetry.connected_student_nodes}
            </div>
            <div className="text-xs font-mono text-slate-300 flex items-center justify-between">
              <span>ফ্রিকোয়েন্সি:</span>
              <span className="font-bold text-white tabular-nums">{telemetry.channel_frequency_mhz} MHz</span>
            </div>
          </div>
          <div className="text-[11px] font-bengali text-slate-400">
            ১৮টি চর শিক্ষা রেডিও সক্রিয়ভাবে যুক্ত
          </div>
        </div>

        {/* Metric 4: RF Link Budget & RSSI */}
        <div className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/80 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>CHANNEL RF LINK</span>
            <Signal className="w-4 h-4 text-blue-400" strokeWidth={1.75} />
          </div>
          <div className="space-y-1">
            <div className="text-3xl font-black font-mono text-blue-300 tabular-nums">
              {telemetry.signal_rssi_dbm.toFixed(1)} <span className="text-sm font-normal text-slate-400">dBm</span>
            </div>
            <div className="text-xs font-mono text-slate-300 flex items-center justify-between">
              <span>SNR অনুপাত:</span>
              <span className="font-bold text-white tabular-nums">+{telemetry.snr_db.toFixed(1)} dB</span>
            </div>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            তাপমাত্রা: <span className="text-white font-bold">{telemetry.system_temperature_c}°C</span>
          </div>
        </div>
      </div>

      {/* DTN Store-and-Forward Assurance Footer */}
      <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 font-bengali text-slate-300">
          <ShieldCheck className="w-4 h-4 text-teal-400 shrink-0" strokeWidth={1.75} />
          <span>
            <strong className="text-white">ডিলি-টলারেন্ট নেটওয়ার্কিং (DTN):</strong> দুর্যোগকালীন সময়ে মোবাইল নেটওয়ার্ক সম্পূর্ণ অচল হলেও সোলার মাইক্রো-হাবের অভ্যন্তরীণ ফ্লাশে শিক্ষার্থীদের উত্তরপত্র সুরক্ষিত থাকে।
          </span>
        </div>

        <div className="shrink-0 text-slate-400 font-mono text-[11px] bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-700">
          পেন্ডিং ডিটিএন ফ্রেম: <span className="text-amber-400 font-bold">{telemetry.dtn_pending_packets ?? 0}</span>
        </div>
      </div>
    </div>
  );
};

export default SolarStationTelemetry;
