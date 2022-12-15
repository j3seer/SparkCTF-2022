const express = require('express')
const puppeteer = require('puppeteer')

const app = express()

module.exports.visitUrl = async function visitUrl(url){
    let browser =
            await puppeteer.launch({
                headless: true,
                pipe: true,
                dumpio: true,
                ignoreHTTPSErrors: true,
                args: [
                    '--no-sandbox',
                    '--disable-background-networking',
                    '--disable-default-apps',
                    '--disable-extensions',
                    '--disable-gpu',
                    '--disable-sync',
                    '--disable-translate',
                    '--hide-scrollbars',
                    '--metrics-recording-only',
                    '--mute-audio',
                    '--no-first-run',
                    '--safebrowsing-disable-auto-update',
                    '--unhandled-rejections=strict'
                ],
            })

    try {
        const ctx = await browser.createIncognitoBrowserContext()
        const page = await ctx.newPage()
        const cookies = [{
            url:url,
            name: 'Flag',
            value: 'SparkCTF{25797b1d3b14bc0eb5f1d4e8143aa797c3e4780cde4f28dc1e3ea831f6a0dd95}',
            domain: 'localhost',
            httpOnly: false,
            samesite: 'strict'
        }];

        try {
            await page.setCookie(...cookies);
            await page.goto(url)
        } finally {
            await page.close()
            await ctx.close()
        }
    }
    finally {
        browser.close()
    }
}
