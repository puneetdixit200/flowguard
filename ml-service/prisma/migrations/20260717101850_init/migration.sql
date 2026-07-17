-- CreateTable
CREATE TABLE "Flow" (
    "id" SERIAL NOT NULL,
    "srcIP" TEXT NOT NULL,
    "dstIP" TEXT NOT NULL,
    "srcPort" INTEGER NOT NULL,
    "dstPort" INTEGER NOT NULL,
    "protocol" TEXT NOT NULL,
    "packetCount" INTEGER NOT NULL,
    "totalBytes" INTEGER NOT NULL,
    "durationSeconds" INTEGER NOT NULL,
    "synCount" INTEGER NOT NULL,
    "ackCount" INTEGER NOT NULL,
    "finCount" INTEGER NOT NULL,
    "rstCount" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Flow_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Alert" (
    "id" SERIAL NOT NULL,
    "flowId" INTEGER,
    "srcIP" TEXT NOT NULL,
    "dstIP" TEXT NOT NULL,
    "protocol" TEXT NOT NULL,
    "severity" TEXT NOT NULL,
    "confidence" TEXT NOT NULL,
    "votes" INTEGER NOT NULL,
    "predictedClass" TEXT NOT NULL,
    "isoForestVerdict" TEXT NOT NULL,
    "rfVerdict" TEXT NOT NULL,
    "aeReconError" DOUBLE PRECISION NOT NULL,
    "explanation" TEXT NOT NULL,
    "threatIntelMatch" BOOLEAN NOT NULL DEFAULT false,
    "threatIntelNote" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Alert_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ThreatIntelEntry" (
    "id" SERIAL NOT NULL,
    "ip" TEXT NOT NULL,
    "category" TEXT NOT NULL,
    "source" TEXT NOT NULL,
    "addedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ThreatIntelEntry_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "ThreatIntelEntry_ip_key" ON "ThreatIntelEntry"("ip");

-- AddForeignKey
ALTER TABLE "Alert" ADD CONSTRAINT "Alert_flowId_fkey" FOREIGN KEY ("flowId") REFERENCES "Flow"("id") ON DELETE SET NULL ON UPDATE CASCADE;
