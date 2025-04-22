import awkward as ak
import correctionlib
import numpy as np
import uproot

import parton

def get_pdfset_conf(pdfname):
    outs = {"pdfname": None,"nReplicas":-1}
    if pdfname == "NNPDF31_nnlo_as_0118_mc_hessian_pdfas":
        # From http://lhapdfsets.web.cern.ch/lhapdfsets/current/NNPDF31_nnlo_as_0118_mc_hessian_pdfas/NNPDF31_nnlo_as_0118_mc_hessian_pdfas.info
        outs["pdfname"]     = "NNPDF31_nnlo_as_0118_mc_hessian_pdfas"
        outs["nReplicas"]   = 103
        outs["iCentral"]    = 0
        outs["iPDF"]        = range(1,101) 
        outs["iAlphaSUp"]   = 101
        outs["iAlphaSDown"] = 102
    if not(outs["pdfname"]):
        raise ValueError("Unknown PDFname %s"%pdfname)
    return outs

def manual_pdf_variations(events, conf):
    """
    Get the matrix element PDF variations manually by evaluating all the PDF
    replicas for the given x, id, Q values for the two partons.
    """
    Q = events.Generator.scalePDF
    id1 = np.where(abs(events.Generator.id1) == 21, 0, events.Generator.id1)
    id2 = np.where(abs(events.Generator.id2) == 21, 0, events.Generator.id2)
    x1 = events.Generator.x1
    x2 = events.Generator.x2
    pdfweights = []
    for i in range(conf["nReplicas"]):
        pdf = parton.mkPDF(conf["pdfname"], i)
        newpdf1 = pdf.xfxQ(id1, x1, Q, grid=False) / x1
        newpdf2 = pdf.xfxQ(id2, x2, Q, grid=False) / x2
        pdfweights.append(newpdf1 * newpdf2)
    pdfweights = np.array(pdfweights).T
    return pdfweights / pdfweights[:, 0][:, np.newaxis]


def get_pdf_alphaS_variations(events, allow_manual=True, pdfname="NNPDF31_nnlo_as_0118_mc_hessian_pdfas"):
    """
    Get the matrix element PDF variations. Only available if there is LHE info.
    If the LHEPdfWeight is not available, the variations are calculated manually.
    This behavior can be disabled by setting allow_manual to False.
    """
    pdfconfig = get_pdfset_conf(pdfname)
    pdf_weights = np.ones(len(events))
    if "LHEPdfWeight" in events.fields:
        if len(events.LHEPdfWeight[0]) > 0:
            pdf_weights = events.LHEPdfWeight
            if ak.max(ak.num(events.LHEPdfWeight, axis=1), axis=0) != pdfconfig["nReplicas"]: 
                """In principle all events have the same number of weights so this is just a dirty way of checking"""
                raise ValueError("Number of weights in LHEPdfWeight %i mismatched with expected %i for PDF set %s. Check that the requested PDF matches the one in your input sample"%(ak.max(ak.num(events.LHEPdfWeight, axis=1), axis=0), pdfconfig["nReplicas"], pdfname))
        elif allow_manual:
            pdf_weights = manual_pdf_variations(events, pdfconfig)
    elif allow_manual:
        pdf_weights = manual_pdf_variations(events, pdfconfig)
    return pdf_weights, pdfconfig
